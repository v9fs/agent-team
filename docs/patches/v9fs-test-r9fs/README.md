# v9fs/test: `r9fs` suite (harness patches)

Two commits for `v9fs/test` on top of `main` `922aacebb637a7e1f366877f039c81073f29a6aa`.
Local branch `cursor/r9fs-suite-f6e3`, head `efba6afa718a70413a61dc9f12fd24a4bd396abb`
(tree `5730052fe94a5f24c1d4a7efebdcb6629606da07`, reproduced by `git am`). Pushing to
`v9fs/test` was refused (`403: Permission to v9fs/test.git denied to cursor[bot]`).

```bash
git checkout -b r9fs-suite 922aacebb637a7e1f366877f039c81073f29a6aa
git am docs/patches/v9fs-test-r9fs/000*.patch
```

| Patch | Scope |
| --- | --- |
| 0001 | `qemu.bash` (devices `r9share` and throttled `r9slow` when `R9FS_SHARE` is set), `scripts/v9fs-run-tests` + `scripts/v9fs-build-initrd` (`r9fs` suite, klog enforced), new `scripts/v9fs-r9fs-tests`, `scripts/v9fs-prepare-r9fs`, `scripts/v9fs-kmod.c`, `scripts/v9fs-build-r9fs-kernel`; README/CHANGES/TODO |
| 0002 | `scripts/v9fs-r9fs-tests`: time the unbind check with shell builtins on guest tmpfs, and record the timings instead of asserting on them |

The suite runs the way the existing suites do. The guest boots the harness initrd, mounts
the container root over C v9fs (`hostshare`) and runs the suite in the Debian chroot. The
suite moves `r9share` and `r9slow` from `9pnet_virtio` to `r9fs_virtio`. The C v9fs view
of the same host directory is the reference.

## Running it

On an arm64 host (as in CI), build the kernel and then run the suite as usual:

```bash
scripts/v9fs-build-r9fs-kernel /path/to/linux ./kernel/.build   # needs clang, rustc+rust-src, bindgen
docker run --rm --privileged --user 0:0 -e KERNELBUILD=/workspaces/kernel/.build \
  -v "$PWD:/home/v9fs-test/test" -v "$PWD/kernel:/workspaces/kernel" -v "$PWD/tmp:/workspaces/tmp" \
  -w /home/v9fs-test/test ghcr.io/v9fs/docker:latest bash -lc "./scripts/v9fs-run-tests r9fs"
```

The recorded runs were on an x86_64 VM. `qemu.bash` only supports `ARCH=aarch64`, and
the guest needs arm64 binaries in the exported root. So the arm64 variant of
`ghcr.io/v9fs/docker` was unpacked to `/tmp/arm64root` with the harness bind mounts.
`v9fs-prepare-r9fs` and `v9fs-build-initrd` ran inside it under qemu-user binfmt.
`run-local-x86.sh` then does what `v9fs-run-tests` does after prepare, with the host's
`qemu-system-aarch64` 8.2.2 instead of the container's. Results:
`docs/reports/r9fs-harness.md`.
