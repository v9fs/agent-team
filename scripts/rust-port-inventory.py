#!/usr/bin/env python3
"""Inventory the kernel surface fs/9p and net/9p consume vs. existing Rust abstractions.

Usage: scripts/rust-port-inventory.py <linux-tree> [--json OUT.json] [--md OUT.md]

The tree needs at least fs/9p, net/9p, include/net/9p, and rust/ checked out.

This is mapping evidence, not proof: call sites are found lexically, so macros
that look like calls are counted, and "referenced from rust/" means the symbol
name appears in rust/kernel, rust/helpers, or rust/bindings, not that a safe
abstraction with the semantics 9p needs exists.
"""

import argparse
import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

NINEP_DIRS = ["fs/9p", "net/9p", "include/net/9p"]
RUST_DIRS = ["rust/kernel", "rust/helpers", "rust/bindings"]

C_KEYWORDS = {
    "if", "for", "while", "switch", "return", "sizeof", "do", "else", "case",
    "typeof", "__typeof__", "defined", "offsetof", "alignof", "_Generic",
    "__attribute__", "__builtin_expect", "asm", "__asm__",
    "int", "void", "char", "long", "short", "unsigned", "signed", "bool",
    "const", "struct", "union", "enum",
}

TABLE_RE = re.compile(
    r"^(?:static\s+)?(?:const\s+)?struct\s+(\w+)\s+(\w+)(?:\s*\[\s*\w*\s*\])?(?:\s+__\w+)*\s*=\s*\{(.*?)\n\};",
    re.S | re.M,
)
FIELD_RE = re.compile(r"\.(\w+)\s*=\s*&?([^,}\n]*)")
FUNC_VALUE_RE = re.compile(r"^[a-z_][a-z0-9_]*$")
CALL_RE = re.compile(r"(?<!->)(?<!\.)\b([A-Za-z_]\w*)\s*\(")
DEF_RE = re.compile(r"^[A-Za-z_][\w\s\*]*?\b(\w+)\s*\([^;{]*\)\s*\{", re.M)
MACRO_RE = re.compile(r"^\s*#\s*define\s+(\w+)", re.M)
COMMENT_RE = re.compile(r"/\*.*?\*/|//[^\n]*", re.S)
STRING_RE = re.compile(r'"(?:\\.|[^"\\])*"')

SUBSYSTEM = {
    "file_system_type": "vfs", "super_operations": "vfs", "inode_operations": "vfs",
    "file_operations": "vfs", "dentry_operations": "vfs",
    "address_space_operations": "vfs/page-cache", "xattr_handler": "vfs/xattr",
    "fs_context_operations": "vfs/mount", "fs_parameter_spec": "vfs/mount",
    "vm_operations_struct": "mm", "netfs_request_ops": "netfs",
    "p9_trans_module": "9p-internal", "virtio_driver": "virtio",
    "virtio_device_id": "virtio", "xenbus_driver": "xen", "xenbus_device_id": "xen", "usb_function_driver": "usb-gadget",
    "usb_function_instance": "usb-gadget", "configfs_item_operations": "configfs",
    "kernel_param_ops": "module", "attribute_group": "sysfs",
    "config_item_type": "configfs",
}


def strip(src: str) -> str:
    return STRING_RE.sub('""', COMMENT_RE.sub(" ", src))


def sources(tree: Path, dirs, exts):
    for d in dirs:
        base = tree / d
        if base.is_dir():
            for p in sorted(base.rglob("*")):
                if p.suffix in exts and p.is_file():
                    yield p


def git_head(tree: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(tree), "rev-parse", "HEAD"], text=True
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("tree", type=Path)
    ap.add_argument("--json", type=Path)
    ap.add_argument("--md", type=Path)
    args = ap.parse_args()
    tree = args.tree.resolve()

    for d in NINEP_DIRS + ["rust/kernel"]:
        if not (tree / d).is_dir():
            print(f"missing {d} under {tree}", file=sys.stderr)
            return 2

    rust_tokens = set()
    rust_files = list(sources(tree, RUST_DIRS, {".rs", ".c", ".h"}))
    for p in rust_files:
        rust_tokens.update(re.findall(r"\b\w+\b", p.read_text(errors="replace")))

    local_defs = set()
    c_files = list(sources(tree, NINEP_DIRS, {".c", ".h"}))
    stripped = {p: strip(p.read_text(errors="replace")) for p in c_files}
    for src in stripped.values():
        local_defs.update(DEF_RE.findall(src))
        local_defs.update(MACRO_RE.findall(src))

    tables = []
    calls = defaultdict(lambda: defaultdict(int))
    for p, src in stripped.items():
        rel = str(p.relative_to(tree))
        for m in TABLE_RE.finditer(src):
            stype, name, body = m.groups()
            fields = FIELD_RE.findall(body)
            if not fields and stype not in SUBSYSTEM:
                continue
            callbacks = [
                f for f, v in fields
                if FUNC_VALUE_RE.match(v.strip()) and v.strip() not in ("true", "false")
            ]
            tables.append({
                "file": rel, "struct": stype, "name": name,
                "subsystem": SUBSYSTEM.get(
                    stype, "usb-gadget" if stype.startswith("usb_") else "other"),
                "fields": len(fields), "callbacks": len(callbacks),
                "rust_references_struct": stype in rust_tokens,
            })
        if p.suffix == ".c":
            top = rel.split("/")[0] + "/9p"
            for fn in CALL_RE.findall(src):
                if fn in C_KEYWORDS or fn in local_defs or fn.startswith("va_"):
                    continue
                if fn.upper() == fn:
                    continue
                calls[fn][top] += 1

    ext = []
    for fn, by_dir in sorted(calls.items()):
        ext.append({
            "symbol": fn, "sites": dict(by_dir), "total": sum(by_dir.values()),
            "in_rust": fn in rust_tokens,
        })

    def summary(prefix):
        rows = [e for e in ext if prefix in e["sites"]]
        covered = [e for e in rows if e["in_rust"]]
        return {"symbols": len(rows), "in_rust": len(covered)}

    fs_abstractions = sorted(
        str(p.relative_to(tree)) for p in (tree / "rust/kernel/fs").glob("*.rs")
    ) if (tree / "rust/kernel/fs").is_dir() else []

    result = {
        "head": git_head(tree),
        "c_files": len(c_files),
        "c_lines": sum(p.read_text(errors="replace").count("\n") for p in c_files),
        "rust_kernel_fs": fs_abstractions,
        "tables": tables,
        "external_calls": {"fs/9p": summary("fs/9p"), "net/9p": summary("net/9p")},
        "external_symbols": ext,
    }

    if args.json:
        args.json.write_text(json.dumps(result, indent=1, sort_keys=True) + "\n")

    md = render_md(result)
    if args.md:
        args.md.write_text(md)
    else:
        sys.stdout.write(md)
    return 0


def render_md(r) -> str:
    out = [
        "# v9fs Rust Port Surface Inventory",
        "",
        f"Generated by `scripts/rust-port-inventory.py` from linux `{r['head']}`.",
        "Lexical mapping evidence only: all-caps macros and `->`/`.` member calls are",
        "excluded from symbol counts; function-valued fields are lowercase bare identifiers.",
        "",
        f"- 9p C files scanned: {r['c_files']} ({r['c_lines']} lines)",
        f"- `rust/kernel/fs/` modules: {', '.join('`'+p.split('/')[-1]+'`' for p in r['rust_kernel_fs']) or 'none'}",
    ]
    for d, s in r["external_calls"].items():
        pct = 100 * s["in_rust"] // max(s["symbols"], 1)
        out.append(
            f"- `{d}` external call symbols: {s['symbols']}, named anywhere in rust/: "
            f"{s['in_rust']} ({pct}%)"
        )
    out += [
        "",
        "## Operation tables",
        "",
        "| Subsystem | Struct | Instance | File | Initialized fields | Function-valued fields | Struct named in rust/ |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for t in sorted(r["tables"], key=lambda t: (t["subsystem"], t["struct"], t["name"])):
        out.append(
            f"| {t['subsystem']} | `{t['struct']}` | `{t['name']}` | `{t['file']}` | "
            f"{t['fields']} | {t['callbacks']} | {'yes' if t['rust_references_struct'] else 'no'} |"
        )
    missing = [e for e in r["external_symbols"] if not e["in_rust"]]
    missing.sort(key=lambda e: -e["total"])
    out += [
        "",
        "## Most-used external symbols with no rust/ reference (top 60)",
        "",
        "| Symbol | fs/9p sites | net/9p sites |",
        "| --- | --- | --- |",
    ]
    for e in missing[:60]:
        out.append(
            f"| `{e['symbol']}` | {e['sites'].get('fs/9p', 0)} | {e['sites'].get('net/9p', 0)} |"
        )
    out.append("")
    return "\n".join(out)


if __name__ == "__main__":
    sys.exit(main())
