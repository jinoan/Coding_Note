#!/bin/sh

# sudo apt-get install jq
# sudo apt install expect

cd ~/Desktop/auto_scp
# ARR=$(python3 config.py | jq '.device_list | .[] | .ips | keys | .[]')
# ARR=$(echo $ARR | tr -d '"')

ARR=$(python3 get_ips.py)
echo $ARR

USER=pi
PW=1234
#FILE1=/home/pi/Desktop/auto_scp/scp_test
FILE1=/home/pi/Desktop/config.py
FILE2=/home/pi/Desktop/cam.py
FILE3=/home/pi/Desktop/lc.py
SAVE_DIR=/home/pi/Desktop/raspberry_PI/.
for IPS in $ARR;
do
#echo $IPS
IP=192.168.0.$IPS
expect<<EOF
  set timeout 2
  spawn scp -o StrictHostKeyChecking=no $FILE1 $FILE2 $FILE3 $USER@$IP:$SAVE_DIR
  expect "password:"
  send "$PW\r"
  expect eof
EOF
done

