#!/usr/bin/env bash
# Local x86 adapter for `scripts/v9fs-run-tests r9fs`: the exported root is the arm64
# ghcr.io/v9fs/docker rootfs (/tmp/arm64root, harness bind mounts in place) and the host's
# qemu-system-aarch64 runs the guest. Prepare + initrd were run in that rootfs beforehand.
set -uo pipefail
R=/tmp/arm64root
cd /tmp/v9fs-test
ts="${TIMESTAMP:-$(date +%s)}"
mkdir -p "logs/$ts"
rm -f logs/guest.exitcode logs/guest.log logs/dmesg.log logs/r9fs.log
export ARCH=aarch64 KERNELBUILD=/tmp/build-arm64 INITRD=$R/workspaces/tmp/initrd.r9fs.cpio
export FSDEV_PATH=$R R9FS_SHARE=$R/workspaces/tmp/r9fs-share
export QEMULOG="logs/$ts/qemu.log" PIDFILE=/tmp/r9fs-qemu.pid
export EXTRA_APPEND="v9fs.ts=$ts v9fs.tests=r9fs"
export QEMU_DAEMONIZE=0 QEMU_STREAM_LOG=0
timeout --foreground "${WAIT_SECS:-2400}" ./qemu.bash < /dev/null > "$QEMULOG" 2>&1
echo "qemu rc=$?"
for f in guest.exitcode guest.log dmesg.log r9fs.log ref.manifest r9fs.manifest; do
  [ -f "logs/$f" ] && cp -f "logs/$f" "logs/$ts/"
done
./scripts/v9fs-scan-klog --suite r9fs --json "logs/$ts/klog.json" "$QEMULOG" "logs/$ts/dmesg.log"
echo "klog rc=$?"
echo "guest rc=$(cat "logs/$ts/guest.exitcode" 2>/dev/null || echo missing)"
echo "logs at /tmp/v9fs-test/logs/$ts"
