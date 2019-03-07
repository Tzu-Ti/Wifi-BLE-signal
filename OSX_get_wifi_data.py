# import package
import subprocess
import time
import datetime
import math
import re
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

# initalize variable
rssi_list = []
label = []
i = 1
previous_minute = 0
people = int(input("How many people in this space: "))

# get wifi signal
time.sleep(60)
while True:
    nowtime = datetime.datetime.now()
    if not nowtime.minute == previous_minute:
        print("minute:", nowtime.minute, "i:", i)
        previous_minute = nowtime.minute
    
    process = subprocess.Popen(['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport','-s'], stdout=subprocess.PIPE)
    out, err = process.communicate()
    process.wait()
    bbsid_re = re.compile("((?:[0-9a-zA-Z]{2}:){5}(?:[0-9a-zA-Z]){2})")
    wifi0 = -100
    wifi1 = -100
    wifi2 = -100
    wifi3 = -100
    wifi4 = -100
    wifi5 = -100
    for line in out.decode("utf8").split("\n"):
        if line.strip().startswith("SSID BSSID"):
            continue
        elif line:
            #ssid
            ssid = bbsid_re.split(line)[0].strip()
            #bssid
            bssid = bbsid_re.split(line)[1]
            #rssi
            rssi = int(bbsid_re.split(line)[-1].strip().split()[0])
#             print(ssid, rssi, bssid)
#             58:d5:6e:e4:f7:61 -> Wei
#             58:d5:6e:e4:f7:62 -> Wei_5G
#             c8:d3:a3:8d:04:cf -> clc-home-1F
#             4c:ed:fb:d3:de:88 -> ASUS
#             bc:54:fc:91:ca:44 -> MH-2Fm
#             00:1e:94:03:81:60 -> 4GSmartCity
            if bssid == "58:d5:6e:e4:f7:61":
                wifi0 = rssi
            elif bssid == "58:d5:6e:e4:f7:62":
                wifi1 = rssi
            elif bssid == "c8:d3:a3:8d:04:cf":
                wifi2 = rssi
            elif bssid == "4c:ed:fb:d3:de:88":
                wifi3 = rssi
            elif bssid == "bc:54:fc:91:ca:44":
                wifi4 = rssi
            elif bssid == "00:1e:94:03:81:60":
                wifi5 = rssi
    rssi_list.append([wifi0, wifi1, wifi2, wifi3, wifi4, wifi5])
    label.append(people)
    
    if i == 500:
        break
    i = i + 1
	
# save numpy array of data
np_rssi_list = np.array(rssi_list)
np_label = np.array(label)

np.save(people + "label", np_label)
np.save(people + "rssi", np_rssi_list)
