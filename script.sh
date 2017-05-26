#!/bin/bash

pvcreate -ff /dev/sdb
vgchange -a n my_vgroup
vgremove my_vgroup
vgchange -a y my_vgroup
vgcreate my_vgroup /dev/sdb
s=$(lsblk | sed -n -r -e 's/.*(sda[0-9]).* ([\.0-9]+)([A-Z]).*$/\1 \2 \3/p')
i=0
for a in $s; do
	if [ $i -eq 0 ]; then
		name=l$a
	fi
	if [ $i -eq 1 ]; then
		sz=$(bc <<< "$a * 1.5")
	fi
	if [ $i -eq 2 ]; then
		lvcreate my_vgroup -n $name -L$sz$a
	fi
	i=$(bc <<< "($i + 1) % 3");
done
lvcreate my_vgroup -n ltmp -L1G
size=$(du -h -s /home | grep -oP '.*\t')
num=$(bc <<< "1.5 * $(grep -oP '[\.0-9]+' <<< $size)")
suf=$(grep -oP '[A-B]' <<< $size)
size=$num$suf
lvcreate my_vgroup -n lhome -L$size
mkfs.ext4 /dev/my_vgroup/ltmp
mkfs.ext4 /dev/my_vgroup/lhome
s=$(blkid | sed -n -r -e 's/.*\/(sda[0-9]).*TYPE="([a-z0-9]+)" .*$/\1 \2/p')
i=0
for a in $s; do
	if [ $i -eq 0 ]; then
		name=$a
	fi
	if [ $i -eq 1 ]; then
		if [[ $a = swap ]]; then
			mkswap /dev/my_vgroup/l$name
		else
			mkfs.$a /dev/my_vgroup/l$name
		fi
		dd if=/dev/$name of=/dev/my_vgroup/l$name bs=1M
		ID=$(blkid | grep -oP "/dev/$name.* UUID=\"\K[a-z0-9\-]+")
		dir=$(df -h | grep -oP "/dev/$name.* /\K[a-zA-Z0-9]+")
		echo "$ID $dir"
		if [[ $dir != boot ]]; then
			sed -i -r -e "s/(UUID=$ID|\/dev\/$name)/\/dev\/my_vgroup\/l$name/g" /etc/fstab
		fi
	fi
	i=$(bc <<< "($i + 1) % 2")
done
mount /dev/my_vgroup/ltmp /mnt
cd /tmp
tar cf - . | (cd /mnt && tar xf -)
umount /mnt
mount /dev/my_vgroup/lhome /mnt
cd /home
tar cf - . | (cd /mnt && tar xf -)
umount /mnt
a=$(grep -oP 'ltmp' /etc/fstab)
if [[ $a != ltmp ]]; then
	cat >> /etc/fstab <<< "/dev/my_vgroup/ltmp /tmp ext4 defaults 0 0"
fi
a=$(grep -oP 'lhome' /etc/fstab)
if [[ $a != lhome ]]; then
	cat >> /etc/fstab <<< "/dev/my_vgroup/lhome /home ext4 defaults 0 0"
fi
