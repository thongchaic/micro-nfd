import time 
import network

# wlan = network.WLAN(network.STA_IF)
# wlan.active(True)
# wlan.connect("TC","aabbccddee")
# while not wlan.isconnected():
#     print(".",end=" ")
#     time.sleep(2)
# print("")
# print(wlan.ifconfig())

#import os
#os.remove('data.csv')

from nfd import MicroNFD

nfd = MicroNFD()
nfd.gateway()

