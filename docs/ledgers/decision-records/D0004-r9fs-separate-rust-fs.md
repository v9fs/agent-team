# Decision Record

- ID: D0004
- Date: 2026-10-08
- Status: Accepted (human steering), merge into `v9fs/linux` still requires human approval
- Decision: Build `r9fs`, a separate read-only Rust 9P2000.L file system module over
  virtio. It carries its own out-of-tree Rust VFS and virtio bindings on a `v9fs/linux`
  topic branch. The C `fs/9p` and `net/9p` stay untouched.

## Context

D0003 recommended an incremental, leaf-first port inside `net/9p` with no out-of-tree
abstractions, because mainline lacks Rust superblock/inode/dentry, netfs and virtio
bindings (E0009, E0010). The human then steered: "implement what we can in rust
providing our own bindings for vfs calls that don't yet exist. This should be its own
filesystem with loadable modules (let's call it r9fs) - stick with just virtio
transport initially", and "Keep everything on a branch in v9fs/linux".

That steering supersedes D0003's "no out-of-tree abstractions" and "VFS gated on
upstream" clauses for this stream. D0003's leaf-first analysis remains valid input for
any later in-place port.

## Options

| Option | Benefits | Costs and risks |
| --- | --- | --- |
| A. Keep D0003 (leaf-first in `net/9p`, upstream-gated) | Mirror stays rebase-clean; no kernel-wide API ownership | Contradicts the human steering; no runnable Rust file system until upstream merges VFS bindings |
| B. Separate `r9fs` module with local bindings on a topic branch | Runnable end to end now; C stack untouched, so no regression surface for `9p`; bindings become concrete upstream requirements | Out-of-tree `rust/kernel/{fs,virtio}` must be rebased with mainline; may diverge from the eventual upstream API (R0004) |
| C. Rewrite `fs/9p` in place in Rust | Single implementation | Replaces production code; needs write/mmap/netfs/cache parity before any value; breaks the mirror |

## Outcome

B. It is the option the human asked for. The topic branch, not `upstream`/`master`,
carries the non-upstream code, so the mirror branches stay rebase-clean. The first
cut covers only the read-only surface: version, attach, walk, getattr, lopen, read,
readdir, readlink, statfs and clunk. That keeps the new binding surface small enough
to review.

## Verification

- Static: clean `LLVM=1` build with `CONFIG_KASAN=y` and `CONFIG_PROVE_LOCKING=y`,
  with no warnings in `rust/kernel/{fs,virtio}` or `fs/r9fs`.
- Contract/Golden: P0006, `docs/reports/r9fs-virtio-smoke.md`. The guest manifest over
  the r9fs mount is diffed against the host manifest, plus negative mount/write cases.
- Independent review of the kernel series before any human merge request.

## Revisit When

- The `cursor/r9fs-rust-virtio-f6e3` branch cannot be pushed to `v9fs/linux` by an agent
  token (currently 403). A human must push it or grant access.
- Mainline merges Rust superblock/inode or virtio abstractions. Then rebase `r9fs`
  onto them and drop the local bindings.
- The work moves beyond read-only (writes, page cache, mmap). Each step needs a new
  slice and binding review.
- `r9fs` is run under a `v9fs/test` harness suite. That would promote it to
  Integration.
