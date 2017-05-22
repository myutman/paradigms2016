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

