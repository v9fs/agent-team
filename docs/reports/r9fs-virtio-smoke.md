# r9fs virtio smoke run (P0006)

## Versions

| Item | Value |
| --- | --- |
| Kernel base | mainline `0c2669a9f4a1d607e7591ae50ccf3c432a0aff08` |
| r9fs series | `docs/patches/linux-r9fs/0001..0006`; branch head `9ee8f93a3439077e2946d5880f3e31cc5ef1255d` (tree `e8b49fb97c10828b28df80e117c5f68ba99bd66e`, reproduced by `git am`) |
| Toolchain | `LLVM=1`, rustc 1.99.0 (`RUSTUP_TOOLCHAIN=stable`) |
| Config | `CONFIG_RUST=y`, `CONFIG_R9FS_FS=m`, `CONFIG_KASAN=y`, `CONFIG_PROVE_LOCKING=y`, `CONFIG_FRAME_WARN=4096`, C `9P_FS`/`NET_9P`/`NET_9P_VIRTIO` = m (not loaded) |
| VMM | QEMU, TCG (`-accel tcg`), `-virtfs local,path=/tmp/share,mount_tag=share,security_model=none` |
| Date | 2026-10-08 |

`CONFIG_FRAME_WARN=4096` works around an unrelated clang+KASAN `-Werror` stack-frame
error in `fs/coredump.c:vfs_coredump`. KVM in this VM started QEMU but produced no
serial output, even with `earlyprintk`, so the run used TCG.

## Commands

```bash
# Build host fixture and reference manifest (reducer)
mkdir -p /tmp/share/sub /tmp/share/many && cd /tmp/share
echo "hello r9fs" > hello.txt; head -c 3000000 /dev/urandom > big.bin
ln -s hello.txt link; ln -s sub/deep dangling; echo deep > sub/deep.txt; mkfifo fifo
for i in $(seq 1 600); do echo $i > many/file_with_a_reasonably_long_name_$i; done
find . -type f -o -type l | sort | while read f; do
  if [ -L "$f" ]; then echo "L $f $(readlink "$f")";
  else echo "F $f $(sha256sum < "$f" | cut -c1-16) $(stat -c %s "$f")"; fi
done > /tmp/host.manifest

# Guest: initramfs = static busybox + r9fs.ko + docs/patches/linux-r9fs/r9fs-smoke-init.sh as /init
qemu-system-x86_64 -accel tcg -m 2G -smp 2 -nographic -no-reboot \
  -kernel bzImage -initrd initramfs.cpio.gz \
  -append "console=ttyS0 earlyprintk=serial,ttyS0 panic=-1" \
  -virtfs local,path=/tmp/share,mount_tag=share,security_model=none,id=fs0 > qemu.log

# Compare
sed -n '/MANIFEST-BEGIN/,/MANIFEST-END/p' qemu.log | tr -d '\r' | grep -E '^(F|L) ' > guest.manifest
diff /tmp/host.manifest guest.manifest
```

The guest computes its manifest with the same reducer, running over the r9fs mount.
The host manifest comes from the host file system directly, so the two sides are
obtained independently. Committed artifact: `r9fs-virtio-smoke.host-manifest.txt`.
The serial console log is a raw runner log (`docs/reports/**/*.log` is gitignored).
The results below are copied from it. The fixture `big.bin` is random, so a rerun
produces different hashes. The diff is the measured result, not the hash values.

## Results

The results are from the run on 0001..0006. The earlier runs on 0001..0004 and 0001..0005
gave the same results, except for the remount rows, which were added after review. On
0005, `remount,rw` failed with EROFS. 0006 switched to the erofs/squashfs convention, so it
now succeeds and the mount stays `ro`.

| Check | Observation | Verdict |
| --- | --- | --- |
| C 9p stack absent | `/proc/modules` has no `9p`/`9pnet`; `r9fs_virtio` listed in `/sys/bus/virtio/drivers` | r9fs owns the device |
| Manifest | 605 rows guest = 605 rows host, `diff` empty (sha256 prefix + size for 603 files incl. 3 MB `big.bin`; target for 2 symlinks) | pass |
| Readdir across batches | `ls /mnt/many | wc -l` = 600 at `msize=65536` | pass |
| `stat` | `hello.txt 11 757411 1 644`, `sub 4096 757241 2 755`, `link 9 757413 1 777`, `fifo 0 757416 1 644`; host `stat` identical (size, inode, nlink, mode) | pass |
| Types | regular, directory, symbolic link, fifo reported by guest `stat -c %F` | pass |
| `df` | guest 265625940 / 15043320 / 250566240 KiB; host 265625944 / 15043320 / 250566240 (0001..0004 run, both sides sampled within seconds) | pass (4 KiB rounding on total) |
| Symlink follow / dangling / missing | `cat link` = `hello r9fs`; dangling rc=1; missing name rc=1 | pass |
| Negative: unknown tag | `mount -t r9fs nosuchtag` → `No such file or directory` | pass |
| Negative: bad option | `-o bogus=1` and `-o trans=tcp` → `Invalid argument`, dmesg `r9fs: unsupported mount option` | pass |
| Negative: second mount of a claimed tag | `Device or resource busy` | pass |
| Negative: writes | `touch`, `>>`, `mkdir` → `Read-only file system`; mount shows `ro` | pass |
| Negative: `remount,rw` | `mount -o remount,rw /mnt` rc=0 and `/proc/mounts` still `ro,relatime`; `remount,noatime` rc=0 and the mount shows `ro,noatime` | pass |
| Negative: setattr after remount attempt | `chmod 600` on `hello.txt` and `fifo` → `Read-only file system`; `stat %a` still 644 for both | pass |
| Parallel reads | 8 concurrent `sha256sum big.bin` → 1 distinct digest | pass |
| Lifecycle | umount, remount, rmmod, insmod, mount, read, umount, rmmod all rc=0 | pass |
| Sanitizers | no `BUG:`, `WARNING:`, `KASAN`, `circular locking`, `possible recursive`, or `Call Trace` in the full console. In both runs the init script's own check reported `dmesg_clean rc=1`. That is a false positive: its pattern matched the boot banner `RCU lockdep checking is enabled`. The committed script uses the narrower pattern | pass |

## Discriminating observations

- A fallback to the C `9p` client would show `9pnet_virtio` in `/proc/modules`. The
  mount would also report type `9p`, not `r9fs`.
- A readdir that ignored the offset cookie would loop or under-count `many/`. It
  would show as a count other than 600, the `EIO` progress guard firing, or missing
  manifest rows.
- A read path that dropped or reordered chunks larger than `msize` would change the
  `big.bin` hash. So would a broken bounce buffer.
- Synthetic attributes would not match the host inode numbers or nlink.
- Without the `reconfigure` op, `remount,rw` cleared `ro` and `simple_setattr` changed the
  in-memory mode. The `/proc/mounts` and `chmod`/`stat` rows catch that.

## Outside the claim

Not tested: writes of any kind, mmap/exec, page cache, xattrs/ACLs, the `v9fs/test`
harness suites, KVM, hot-unplug of the device while mounted or during an RPC, a
hostile or malformed 9P server (no `Rlerror` errno injection was run), virtio-mmio and
probe-failure paths (the review fixes in 0005/0006 for those, and for kick failure and
foreign-superblock inodes, are code-review only), signal interruption of a stuck request, multiple
virtio-9p devices, coexistence with the C `9pnet_virtio` driver, and performance.
