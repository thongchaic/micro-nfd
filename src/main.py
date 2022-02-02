from nfd import MicroNFD
import time 
import network

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("PNHome2","st11ae58*")
while not wlan.isconnected():
    print(".",end=" ")
    time.sleep(2)
print("")
print(wlan.ifconfig())

# nfd = MicroNFD()
# nfd.gateway()

# w=5
# while w>0:
#     time.sleep(1)
#     print("w:",w)
#     w=w-1

# nfd.mote()
