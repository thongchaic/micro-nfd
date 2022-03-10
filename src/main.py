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

#---------- MQTT Face Test ------------
# from config import * 
# from mqtt import MQTTx
# mqttx = MQTTx(2,123,mqtt_config)
# mqttx.add('/ndn/alice')

# while True:
#     mqttx.receive()

from nfd import MicroNFD
nfd = MicroNFD()

# n=5
# while n > 0:
#     print('.', end=" ")
#     time.sleep(1)
#     n = n - 1 
    
# if nfd.mode == 1:
#     nfd.mote()