#!/bin/bash

cat > /boot/grub/custom.cfg <<< "submenu 'Extra menu' {"

foo (){
	grep -oP "vmlinuz-\K.*" <<< $1
}

f=`find /boot -name "vmlinuz-*"`
UUID=$(grep -oP "UUID=\K.*(?= / )" /etc/fstab)
for a in $f; do
	tmp=$(foo $a)
	cat >>  /boot/grub/custom.cfg <<< "
	menuentry 'Ubuntu $tmp'{
		recordfail
		load_video
		insmod gzio
		if [ x$grub_platform = xxen ]; then insmod xzio; insmod lzopio; fi
		insmod part_msdos
		insmod ext2
		set root='hd0,msdos1'
		linux /vmlinuz-$tmp root=UUID=$UUID ro
		initrd /initrd.img-$tmp
	}"
done

cat >> /boot/grub/custom.cfg <<< "}"
update-grub

