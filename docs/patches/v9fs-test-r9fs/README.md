# v9fs/test: `r9fs` suite (harness patches)

Four commits for `v9fs/test` on top of `main` `922aacebb637a7e1f366877f039c81073f29a6aa`.
Local branch `cursor/r9fs-suite-f6e3`, head `0a17192a471680fe90cf13ce6e97f0762190f424`
(tree `bfe9f9d3f58516256c479d235a1cc6679ed12436`, reproduced by `git am`). The 0001..0002
head was `efba6afa718a` (tree `5730052fe94a`). Pushing to
`v9fs/test` was refused (`403: Permission to v9fs/test.git denied to cursor[bot]`).

```bash
git checkout -b r9fs-suite 922aacebb637a7e1f366877f039c81073f29a6aa
git am docs/patches/v9fs-test-r9fs/000*.patch
```

| Patch | Scope |
| --- | --- |
| 0001 | `qemu.bash` (devices `r9share` and throttled `r9slow` when `R9FS_SHARE` is set), `scripts/v9fs-run-tests` + `scripts/v9fs-build-initrd` (`r9fs` suite, klog enforced), new `scripts/v9fs-r9fs-tests`, `scripts/v9fs-prepare-r9fs`, `scripts/v9fs-kmod.c`, `scripts/v9fs-build-r9fs-kernel`; README/CHANGES/TODO |
| 0002 | `scripts/v9fs-r9fs-tests`: time the unbind check with shell builtins on guest tmpfs, and record the timings instead of asserting on them |
| 0003 | `.github/workflows/r9fs.yml` (manual, `ubuntu-24.04-arm`): toolchain (`scripts/v9fs-install-rust-toolchain`), Rust kernel build, `v9fs-run-tests r9fs`, logs artifact; `R9FS_KO` override in prepare; `r9fs.log` kept in `logs/<ts>/` |
| 0004 | `scripts/v9fs-r9fs-tests`: the reference manifest, statfs and checksum come from C v9fs mounting `r9share` itself (same msize) before the device moves to r9fs. Harness CI's QEMU 10.0 remaps qid paths on `hostshare`, so inode numbers through `hostshare` differ from `r9share` whatever the client |

The suite runs the way the existing suites do. The guest boots the harness initrd, mounts
the container root over C v9fs (`hostshare`) and runs the suite in the Debian chroot. The
suite first takes its reference from C v9fs mounting `r9share`, then moves `r9share` and
`r9slow` from `9pnet_virtio` to `r9fs_virtio`.

## Running it

In `v9fs/test` Actions, after a human pushes the kernel branch and these patches, run it by
hand:

```bash
gh workflow run r9fs.yml -f linux_repository=v9fs/linux -f linux_ref=cursor/r9fs-rust-virtio-f6e3
```

On any arm64 host, build the kernel and then run the suite as usual:

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
