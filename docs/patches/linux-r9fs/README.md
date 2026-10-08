# r9fs: Rust 9P2000.L file system over virtio (v9fs/linux branch)

Kernel branch `cursor/r9fs-rust-virtio-f6e3` for `v9fs/linux`, based on mainline
`0c2669a9f4a1d607e7591ae50ccf3c432a0aff08` (Merge tag 'soc-fixes-7.3-2', 2026-10-08).
Branch head: `ce42b3c71d53a1882d658a4954d39ab991c11124` (tree `8d614e9ff4ba7f1af5279b0a077c01a6c50fa28b`).
The slice-1 head (0001..0006) was `9ee8f93a3439077e2946d5880f3e31cc5ef1255d`.

Pushing that branch to `v9fs/linux` was refused (`403: Permission to v9fs/linux.git
denied to cursor[bot]`). This series is a byte-exact copy of the branch made with
`git format-patch 0c2669a9f..ce42b3c71`, so a maintainer can recreate it:

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
| 0005 | fs: r9fs: harden against server errnos, dead channels and remount,rw | review response 1: `fs/r9fs/`, `rust/kernel/{fs/*,virtio}.rs` |
| 0006 | rust: virtio, fs: avoid double del_vqs and keep remount read-only | review response 2: `rust/kernel/{virtio,fs/filesystem}.rs`, `rust/helpers/virtio.c` |
| 0007 | fs: r9fs: make RPC waits killable and wake waiters on device removal | slice 2 (R0006): `fs/r9fs/{transport,client}.rs`, `rust/kernel/sync/{completion.rs,lock/mutex.rs}`, `rust/helpers/mutex.c` |
| 0008 | rust: fs, virtio; fs: r9fs: apply rustfmt | no functional change; `make rustfmtcheck` clean |
| 0009 | fs: r9fs: derive inode numbers from qids as fs/9p does | `fs/r9fs/{proto,r9fs}.rs`: `ino = qid.path + 2` (`QID2INO`), found by the `v9fs/test` differential |

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

## arm64 harness build

`docs/patches/v9fs-test-r9fs` (`scripts/v9fs-build-r9fs-kernel`) builds the harness
Image: arm64 `defconfig`, plus the publish workflow's 9p options, plus `RUST=y` and
`R9FS_FS=m`. The C 9p client is built in there and claims every virtio-9p device at boot.
The suite rebinds its devices to `r9fs_virtio` through sysfs. Build `r9fs.ko` from the
same commit as the Image: `CONFIG_LOCALVERSION_AUTO` puts the commit in the vermagic, and
a mismatch fails `finit_module` with `ENOEXEC`.

## Smoke test

`r9fs-smoke-init.sh` is the `/init` of a static-busybox initramfs that also contains
`r9fs.ko`. Results and the reducer are in `docs/reports/r9fs-virtio-smoke.md`.
