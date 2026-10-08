# r9fs under the v9fs/test harness (P0007)

The `r9fs` suite (`docs/patches/v9fs-test-r9fs`) runs like the existing `v9fs/test`
suites. An arm64 QEMU guest boots the harness initrd and mounts the container root through
the C v9fs client (`hostshare`, `cache=loose`). The suite then runs inside the Debian
chroot. QEMU's virtio-9p server also exports one host directory on two more devices:
`r9share`, and `r9slow` with `throttling.bps-read=1024`. The suite rebinds both to
`r9fs_virtio`. The reference for every r9fs observation is the C v9fs client reading the
same host directory through `hostshare`, served by the same QEMU 9p server.

## Versions

| Item | Value |
| --- | --- |
| Kernel | `docs/patches/linux-r9fs/0001..0009`, head `ce42b3c71d53a1882d658a4954d39ab991c11124` on mainline `0c2669a9f4a1` |
| Image | arm64 `defconfig` + publish-workflow 9p options + `RUST=y`, `R9FS_FS=m`, `IKCONFIG_PROC`; `LLVM=1`, rustc 1.99.0; Image sha256 `39c4bf947d47feca8f88efdf7d01a83111f3fc96cacc0e42f3b854ba9ed4bf63` |
| `r9fs.ko` | current `7be73165304eff5ba3ba9b1862ea9f0dc343c4b5fb6b1dc1c096b740f26b2885` (head); control `c61369f74ac68a5d9f4fb029acb3adbbed4510570bab700ad903027082bf6392` (`fs/r9fs` at slice-1 head `9ee8f93a3439`, same Image) |
| Harness | `v9fs/test` `922aacebb637` + `docs/patches/v9fs-test-r9fs/0001..0002` (head `efba6afa718a`) |
| Container | `ghcr.io/v9fs/docker@sha256:017a01a107e69b862013844e95905479007b0860c024a6bb717f0fea5af56224`, arm64 variant |
| VMM | `qemu.bash` arguments; host `qemu-system-aarch64` 8.2.2 under TCG (x86_64 VM, see the patch README) |
| Date | 2026-10-08 |

## Commands

```bash
scripts/v9fs-build-r9fs-kernel /tmp/linux /tmp/build-arm64      # in v9fs/test
# Arm64 rootfs at /tmp/arm64root with the harness bind mounts; then per module:
chroot /tmp/arm64root bash -lc 'cd /home/v9fs-test/test && KERNELBUILD=/workspaces/kernel/.build \
  ./scripts/v9fs-prepare-r9fs && V9FS_TESTS=r9fs ./scripts/v9fs-build-initrd /workspaces/tmp/initrd.r9fs.cpio'
cp r9fs-old-arm64.ko /tmp/v9fs-test/tmp/r9fs/r9fs.ko            # control run only
docs/patches/v9fs-test-r9fs/run-local-x86.sh                    # qemu.bash + v9fs-scan-klog
```

## Results

Guest output: `r9fs-harness/r9fs-ce42b3c7.txt` (current) and
`r9fs-harness/control-r9fs-9ee8f93a.txt` (control).

| Check | Current | Control (slice 1) |
| --- | --- | --- |
| load, rebind both devices, mount | PASS | PASS |
| `manifest-vs-v9fs`: 608 rows (type, mode, nlink, uid, gid, inode, size, mtime, sha256, symlink target) | PASS (identical) | FAIL: every inode is C v9fs − 2 |
| `statfs` (capacity in bytes; QEMU scales `f_bsize` with `msize`) | PASS | PASS |
| `mount(2)` errnos: unknown tag `ENOENT`, `bogus=1` `EINVAL`, claimed tag `EBUSY` | PASS | PASS |
| `EROFS` for create, mkdir, chmod; `remount,rw` stays `ro` | PASS | PASS |
| 8 parallel `sha256sum` of a 3 MB file equal the C v9fs sum | PASS | PASS |
| umount, remount, reread | PASS | PASS |
| `kill-stalled-reader`: reader in D on a posted throttled `Tread`, `kill -9` to reaped | PASS, 20 ms | FAIL, 1790 ms |
| `reply-after-kill`: next request gets its own reply | PASS | PASS |
| `unbind-fails-posted-read`: unbind `r9fs_virtio` with the `Tread` posted | PASS: EIO, 0 bytes after unbind | FAIL: EIO, but 4096 bytes delivered after unbind |
| `EIO` after unbind, umount, unload | PASS | PASS |
| guest exit code / `v9fs-scan-klog` (BUG, WARNING, Oops, hung_task) | 0 / 0 hits | 1 / 0 hits |

## What the discriminating checks show

- **Manifest.** C v9fs uses `qid.path + 2` as the inode number (`QID2INO`). The slice-1
  r9fs used `qid.path` (it matched the host's `st_ino`, which the slice-1 smoke run
  never compared against C). Patch 0009 adopts the C mapping for both `st_ino` and
  `d_ino`. A copied constant or a host-side manifest would not catch this; the C
  client on the same server does.
- **Kill.** Each `read(2)` is one 4 KiB `Tread` (`bs` < `msize`), throttled at 1 KiB/s,
  so exactly one request is posted when the reader is killed. The slice-1 transport
  waits for that reply uninterruptibly (1790 ms ≈ the rest of the request). Patch 0007
  returns at once. The next request reaps the abandoned reply first and still gets its
  own (`reply-after-kill`).
- **Unbind.** The driver's removal is followed by a virtio reset. QEMU's virtio-9p reset
  completes in-flight requests before returning, so the posted `Tread` is completed
  during the reset. A waiter still blocked at that point receives the 4096 bytes (slice
  1). Patch 0007 sets `removed` and calls `complete_all()` before the reset, so the
  waiter fails with `EIO` and the reply is never delivered (0 bytes).

## Non-claims and observations

- **Wake latency under device removal is not measured.** QEMU completes the throttled
  request inside the reset while holding its global lock, and under TCG the whole guest
  stalls until then. `hostshare` stalls too, so tools on the 9p root cannot timestamp
  anything. The unbind took 57.6 s with the current module and 57.5 s with the control;
  the reader exited within 10 ms of it in both. The suite records `unbind_ms` and
  `reader_exit_ms` and asserts neither. The first version timed the reader with `awk`
  on the 9p root and gave the same number for the same reason.
- Not run in Actions: no Rust toolchain in `ghcr.io/v9fs/docker`, no published
  `r9fs.ko`, and no push access to `v9fs/test` (TODO row in patch 0001).
- Recorded on x86_64 with an emulated arm64 guest and host QEMU 8.2.2, not the
  container's QEMU on an arm64 runner.
- No KASAN or lockdep in this Image (harness `defconfig`); the slice-1 smoke run covers
  those on x86_64 for 0001..0006 only.
- Writes, mmap/exec, page cache, xattr/ACL, cache modes, the other harness suites
  (`fsx`, `dbench`, protocol), `Tflush`, true surprise removal (the device always
  completes the request here), and performance.
