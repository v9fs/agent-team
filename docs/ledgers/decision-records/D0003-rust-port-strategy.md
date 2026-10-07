# Decision Record

- ID: D0003
- Date: 2026-10-07
- Status: Proposed (human decision required: this is materially wider scope than A2)
- Decision: Port `fs/9p` and `net/9p` to Rust incrementally, starting with
  C-callable Rust leaf functions in `net/9p` behind a Kconfig option with the C
  code kept. Upstream every new Rust abstraction before v9fs depends on it.
  Never carry out-of-tree abstractions on the `v9fs/linux` mirror branches.
  Transports and `fs/9p` VFS work stay blocked until the needed abstractions
  exist upstream.

## Context

A human asked for a Rust port of the v9fs kernel filesystem (`fs/9p` and
`net/9p`). Pinned evidence (E0009, E0010, and
`docs/reports/rust-port-inventory.md`) shows:

- `v9fs/linux` `upstream` is `602042bf29f6efde39cfb5fdd9289bf4854bc0c5`
  (v7.3-rc6+). It has 33 C files and 15,024 lines in `fs/9p`, `net/9p`, and
  `include/net/9p`.
- `rust/kernel/fs/` contains only `file.rs` and `kiocb.rs`. Mainline has no
  Rust binding for filesystem registration, `fs_context`, superblocks, inodes,
  dentries, address spaces, netfs, fscache, POSIX ACLs, xattr handlers, virtio,
  sockets, Xen grant tables, RDMA, or USB gadget functions.
- None of the 9p operation tables for those subsystems is named in `rust/`.
  The exception is `file_operations`, which `miscdevice` already wraps. The
  inventory found 197 external call symbols in `fs/9p`, of which 19 (9%) are
  named anywhere in `rust/`. In `net/9p` it found 278, of which 68 (24%) are.
- The upstream Rust VFS series (Wedson Almeida Filho; tarfs, ext2, and puzzlefs
  samples) only reached RFC or experimental branches. The merged `vfs rust`
  pulls up to v7.0 add only small infrastructure (E0010).
- There is in-tree precedent for C calling a Rust leaf inside a C subsystem:
  `drivers/gpu/drm/drm_panic_qr.rs` uses `#[export] pub unsafe extern "C" fn`,
  which checks the Rust signature against the bindgen C prototype.
- `v9fs/linux` must stay a rebase-clean mainline mirror (D0002), and agents
  may not merge into it. Issue #6 (t0013) may hold the `v9fs/linux` Image
  config write scope.

## Options

| Option | Benefits | Costs and risks |
| --- | --- | --- |
| A. Rewrite all of `fs/9p` and `net/9p` in Rust at once, on a v9fs branch carrying out-of-tree VFS, netfs, virtio, and socket abstractions | Matches the literal request | v9fs would have to own around 20 kernel-wide abstractions without the relevant maintainers. Breaks the rebase-clean mirror and has no path upstream. Proof only exists at the end and the diff can't be reviewed. Highest risk of data loss and memory-safety regressions during the transition. |
| B. A parallel second Rust filesystem module (for example `rust9p`) next to the C one, like the Rust reference-driver pattern | The C path stays untouched; side-by-side comparison | It still needs every VFS, netfs, and transport abstraction from A before it can mount anything. Upstream accepts duplicate drivers only with explicit maintainer agreement. |
| C. Incremental leaf-first replacement in `net/9p`, behind Kconfig with C kept; abstractions upstreamed first; later phases gated on upstream | Each slice is small and reviewable, with a differential proof against the C implementation it replaces. Starts with the code that parses untrusted server bytes, where Rust's memory safety helps most. No out-of-tree abstractions. | The full port is gated on work outside v9fs's control (VFS, netfs, virtio, socket Rust abstractions). Two implementations coexist for a long time. The Image needs a Rust toolchain. |
| D. Defer until upstream VFS abstractions exist | No cost now | No learning and no harness Rust capability; v9fs would not help shape the abstractions it will need |

## Outcome

Recommend C. A and B both depend on the same missing VFS, netfs, and transport
abstractions, and A would also break the mirror contract. C gives
proof-carrying slices that run against the existing harness, and it pushes
exactly the missing abstractions upstream as concrete requirements.

The first leaf is `p9dirent_read()` (`net/9p/protocol.c`). It has a fixed,
exported ABI (`include/net/9p/client.h`), a single caller
(`fs/9p/vfs_dir.c` 9P2000.L readdir), and parses server-controlled bytes. It
needs no new kernel-wide abstraction beyond adding `net/9p/client.h` to
`rust/bindings/bindings_helper.h`.

## Verification

```bash
python3 scripts/rust-port-inventory.py <linux@602042bf> \
  --md docs/reports/rust-port-inventory.md
scripts/check-scaffold.sh
```

Discriminating observation: if mainline gained `rust/kernel/fs/{super,inode,dentry}.rs`
or a netfs or virtio abstraction, the inventory's `rust_kernel_fs` list and the
"struct named in rust/" column would change. That change would trigger a
revisit of A and B against C.

## Revisit When

- A human rejects or amends this proposal on the program issue.
- Mainline or `vfs.git` merges Rust superblock, inode, or dentry abstractions,
  or Rust netfs, virtio, or socket abstractions (rerun the inventory on the new
  tag).
- The `net/9p` maintainers reject Rust in `net/9p` on list. Stop C and
  record the outcome.
- Two Phase 1 leaves land with differential proof. Then decide whether to
  start Phase 2 (client core).
