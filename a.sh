ct=0
dd if=/dev/zero of=zr bs=1 count=16 2> /dev/null
for (( i=0; i<4; i++ ))
do
	sk=$( expr 446 + $i \* 16 )
	dd if=/dev/sda of=f bs=1 count=16 skip=$sk 2> /dev/null
	if !(cmp f zr > /dev/null); then
		ct=$( expr $ct + 1 )
	fi
done
echo $ct


