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

n=5
while n > 0:
    print('.', end=" ")
    time.sleep(1)
    n = n - 1 
    
if nfd.mode == 1:
    nfd.mote()