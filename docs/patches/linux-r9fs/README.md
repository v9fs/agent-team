# r9fs: Rust 9P2000.L file system over virtio (v9fs/linux branch)

Kernel branch `cursor/r9fs-rust-virtio-f6e3` for `v9fs/linux`, based on mainline
`0c2669a9f4a1d607e7591ae50ccf3c432a0aff08` (Merge tag 'soc-fixes-7.3-2', 2026-10-08).
Branch head: `05b7336f354e52aedfe91da5df98511fca5a7580`.

Pushing that branch to `v9fs/linux` was refused (`403: Permission to v9fs/linux.git
denied to cursor[bot]`). This series is a byte-exact copy of the branch made with
`git format-patch 0c2669a9f..05b7336f3`, so a maintainer can recreate it:

```bash
git checkout -b cursor/r9fs-rust-virtio-f6e3 0c2669a9f4a1d607e7591ae50ccf3c432a0aff08
git am docs/patches/linux-r9fs/000*.patch
git push -u origin cursor/r9fs-rust-virtio-f6e3
```

Do not merge this from `v9fs/agent-team`. Merging into `v9fs/linux` needs human
approval (`AGENTS.md`, D0004).

| Patch | Subject | Scope |
| --- | --- | --- |
| 0001 | rust: sync: completion: add complete() and reinit() | `rust/kernel/sync/completion.rs`, `rust/helpers/completion.c` |
| 0002 | rust: virtio: add a minimal virtio driver binding | `rust/kernel/virtio.rs`, `rust/helpers/virtio.c`, `bindings_helper.h` |
| 0003 | rust: fs: add file system registration, superblock and inode abstractions | `rust/kernel/fs{,/filesystem,/inode}.rs`, `rust/helpers/fs.c` |
| 0004 | fs: r9fs: add read-only Rust 9P2000.L file system over virtio | `fs/r9fs/`, `fs/Kconfig`, `fs/Makefile` |

Note: `rust/helpers/completion.c` is added in 0002, not 0001, so 0001 alone does not
link `reinit()`. The series is bisectable at 0002 and later.

## Build

```bash
export RUSTUP_TOOLCHAIN=stable   # rustc >= 1.85; tested with 1.99.0
make LLVM=1 O=/tmp/build olddefconfig
scripts/config --file /tmp/build/.config -e RUST -m R9FS_FS -m NET_9P -m NET_9P_VIRTIO -m 9P_FS
make LLVM=1 O=/tmp/build -j"$(nproc)" bzImage modules
```

`LLVM=1` is required whenever `CONFIG_KASAN=y`, because `RUST` depends on
`!KASAN || CC_IS_CLANG`. Without it, `CONFIG_RUST` is dropped silently. Keep the C
`9pnet_virtio` driver modular and unloaded, or it may bind the virtio-9p device first.

## Smoke test

`r9fs-smoke-init.sh` is the `/init` of a static-busybox initramfs that also contains
`r9fs.ko`. Results and the reducer are in `docs/reports/r9fs-virtio-smoke.md`.
