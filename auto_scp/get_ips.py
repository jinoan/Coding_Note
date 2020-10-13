import sys
import os
#sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config
device_list = config.refrigerators["device_list"]
ips_list = []
for device in device_list:
    for ip_key in device["ips"].keys():
        print(int(ip_key))

