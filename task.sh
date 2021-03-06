#!/bin/bash

MY_POOL="my_pool"
MY_LOGIN="login"
MY_PASSWORD="password"

mkdir /miner
cd /miner
wget https://github.com/fireice-uk/xmr-stak-cpu/archive/v1.2.0-1.4.1.tar.gz 
tar -xvzf v1.2.0-1.4.1.tar.gz
rm v1.2.0-1.4.1.tar.gz
cd xmr-stak-cpu-1.2.0-1.4.1
sed -i "s/null/\[\n\    { \"low_power_mode\" \: false\, \"no_prefetch\" \: true\, \"affine_to_cpu\" \: 0 \}\,\n    \{ \"low_power_mode\" \: false, \"no_prefetch\" \: true, \"affine_to_cpu\" \: 1 \}\,\n\]/g" config.txt
sed -i "s/pool\.supportxmr\.com\:3333/$MY_POOL/g" config.txt
sed -i "s/\"wallet_address\" \: \"\"/\"wallet_address\" \: \"$MY_LOGIN\"/g" config.txt
sed -i "s/\"pool_password\" \: \"\"/\"pool_password\" \: \"$MY_PASSWORD\"/g" config.txt

yes Y | apt-get install libmicrohttpd-dev libssl-dev cmake build-essential
cmake .
make install

touch /etc/miner.cfg
echo "" > /etc/miner.cfg

touch /miner/start_miner.sh
echo "#!/bin/bash" > /miner/start_miner.sh
echo "key=\$(cat /etc/miner.cfg)" >> /miner/start_miner.sh
echo "cd /miner/xmr-stak-cpu-1.2.0-1.4.1/bin/" >> /miner/start_miner.sh
echo "./xmr-stak-cpu $key" >> /miner/start_miner.sh
chmod +x /miner/start_miner.sh

sed -i "s/exit 0/\/miner\/start_miner\.sh \|\| exit 1/g" /etc/rc.local
echo "exit 0" >> /etc/rc.local