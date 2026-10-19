#!/usr/bin/env python3
"""Compile the project's maintained Markdown summary with Pandoc and Typst."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def render(root: Path) -> dict:
    root = root.resolve()
    source = root / "docs/project-summary.md"
    template = root / "docs/reporting/usenix-summary.typst"
    pdf = source.with_suffix(".pdf")
    receipt = source.with_suffix(".json")
    for path in (source, template):
        if not path.is_file():
            raise RuntimeError(f"Required report input missing: {path}")
    for tool in ("pandoc", "typst"):
        if not shutil.which(tool):
            raise RuntimeError(f"Required report tool missing: {tool}; source and previous PDF preserved")
    source_hash = digest(source)
    template_hash = digest(template)
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root,
                          capture_output=True, text=True)
    status = subprocess.run(["git", "status", "--porcelain"], cwd=root,
                            capture_output=True, text=True)
    # Stage beside the output for atomic replacement; a failed compile leaves
    # the previous PDF and receipt intact. No shell or network fetch is used.
    with tempfile.TemporaryDirectory(prefix=".summary-", dir=source.parent) as tmp:
        staged_pdf = Path(tmp) / "project-summary.pdf"
        subprocess.run([
            "pandoc", str(source), "--standalone", "--to=typst",
            "--pdf-engine=typst", "--template", str(template),
            "--pdf-engine-opt=--root", f"--pdf-engine-opt={root}",
            "--resource-path", os.pathsep.join((str(source.parent), str(root))),
            "--output", str(staged_pdf),
        ], cwd=source.parent, check=True, capture_output=True, text=True)
        if not staged_pdf.is_file() or not staged_pdf.read_bytes().startswith(b"%PDF-"):
            raise RuntimeError("Renderer did not produce a PDF; previous output preserved")
        if source_hash != digest(source) or template_hash != digest(template):
            raise RuntimeError("Report input changed during rendering; previous output preserved")
        result = {
            "built_at": datetime.now(timezone.utc).isoformat(),
            "source_sha256": source_hash,
            "template_sha256": template_hash,
            "pdf_sha256": digest(staged_pdf),
            "build_context_head": head.stdout.strip() if head.returncode == 0 else None,
            "build_context_dirty": bool(status.stdout.strip()) if status.returncode == 0 else None,
            "claim_review": "required",
            "visual_qa": "required",
        }
        staged_receipt = Path(tmp) / "project-summary.json"
        staged_receipt.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        staged_pdf.replace(pdf)
        staged_receipt.replace(receipt)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        print(json.dumps(render(args.root), indent=2))
        return 0
    except (RuntimeError, OSError, subprocess.CalledProcessError) as exc:
        print(f"Report incomplete: {exc}")
        if isinstance(exc, subprocess.CalledProcessError) and exc.stderr:
            print(exc.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
