#!/bin/busybox sh
/bin/busybox --install -s /bin
mount -t proc proc /proc
mount -t sysfs sys /sys
mount -t devtmpfs dev /dev
echo 1 > /proc/sys/kernel/printk_ratelimit 2>/dev/null
r() { echo "RESULT $1 rc=$2"; }

echo "== C 9p modules loaded:"; grep -E '^(9p|9pnet)' /proc/modules || echo none
insmod /r9fs.ko; r insmod $?
grep r9fs /proc/filesystems
ls /sys/bus/virtio/drivers/

mount -t r9fs nosuchtag /mnt 2>/tmp/e; r badtag $?; cat /tmp/e
mount -t r9fs -o bogus=1 share /mnt 2>/tmp/e; r badopt $?; cat /tmp/e
mount -t r9fs -o trans=tcp share /mnt 2>/tmp/e; r badtrans $?; cat /tmp/e

mount -t r9fs -o msize=65536 share /mnt; r mount $?
grep r9fs /proc/mounts
mount -t r9fs share /tmp 2>/tmp/e; r busy $?; cat /tmp/e

cd /mnt
echo "MANIFEST-BEGIN"
find . -type f -o -type l | sort | while read f; do
  if [ -L "$f" ]; then echo "L $f $(readlink "$f")"; else echo "F $f $(sha256sum < "$f" | cut -c1-16) $(stat -c %s "$f")"; fi
done
echo "MANIFEST-END"
cd /
r count_many "$(ls /mnt/many | wc -l)"
stat -c 'STAT %n %s %i %h %F %a' /mnt/hello.txt /mnt/sub /mnt/link /mnt/fifo
cat /mnt/link; r cat_link $?
cat /mnt/dangling 2>/dev/null; r cat_dangling $?
cat /mnt/nope 2>/dev/null; r enoent $?
df /mnt | tail -1
touch /mnt/new 2>/tmp/e; r write_touch $?; cat /tmp/e
echo x >> /mnt/hello.txt 2>/tmp/e; r write_append $?; cat /tmp/e
mkdir /mnt/d 2>/tmp/e; r mkdir $?; cat /tmp/e

for i in 1 2 3 4 5 6 7 8; do (sha256sum /mnt/big.bin > /tmp/par.$i) & done; wait
r parallel "$(cat /tmp/par.* | cut -d' ' -f1 | sort -u | wc -l)"

umount /mnt; r umount $?
mount -t r9fs share /mnt; r remount $?
cat /mnt/hello.txt
umount /mnt
rmmod r9fs; r rmmod $?
insmod /r9fs.ko; r reinsmod $?
mount -t r9fs share /mnt; r mount2 $?
cat /mnt/sub/deep.txt
umount /mnt; rmmod r9fs; r rmmod2 $?

echo "== dmesg check"
dmesg | grep -E 'BUG|WARNING|KASAN|lockdep|circular|possible recursive|leak' && r dmesg_clean 1 || r dmesg_clean 0
echo DONE
poweroff -f
