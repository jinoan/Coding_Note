cd ~/Desktop/auto_scp
ARR=$(python3 get_ips.py)
echo $ARR
USER=pi
PW=1234
for IPS in $ARR;
do
#echo $IPS
IP=192.168.0.$IPS
expect<<EOF
  set timeout 1
  spawn ssh $USER@$IP "sudo reboot"
  expect "password"
  send "$PW\r"
  expect eof
EOF
done

