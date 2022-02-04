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

from nfd import MicroNFD

nfd = MicroNFD()
nfd.gateway()

