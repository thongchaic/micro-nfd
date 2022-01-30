#      ^^
#     (oo)
#    /(__)\
#  -------------
#  < MicroNFD >
#  -------------     
#  Experimented on TTGOv1.0 ESP32 LoRa 

import time 
import urandom 
import ubinascii
import machine
from fw import Forwarder
# from wifi_manager import WifiManager
from config import * 
from experiments import ExperimentalData

# class MicroNFD(object):
#     def __init__(self,config="config.py"):
#         self.UUID = ubinascii.hexlify( machine.unique_id() ).decode()
#         #read config 
#         # self.manager = WifiManager(wifi_config)
#         # self.manager.connect()
#         # self.fwd = Forwarder(self.UUID,device_config)
#         #The haunting of MicroNFD's daemon 
#         # self.nfd.daemon()
    
class MicroNFD(object):
    # 1 Gw
    # 0 Sensor
    def __init__(self,role=0):
        self.UUID = ubinascii.hexlify( machine.unique_id() ).decode()
        # self.manager = WifiManager(wifi_config)
        # self.manager.connect()
        self.exp = ExperimentalData("data.csv")
        self.fwd = Forwarder(self.UUID, device_config, lora_parameters, app_config)
        d
    def nfdc(self):
        #Easy to manage partial name  

        self.fwd.addRoute(1,"/alice/join")
        #self.fwd.addRoute(1,"/alice/light/status")

    def joinInterst(self):
        #NDN-LPWAN JoinInterest Procedure 
        nonce = str(urandom.random())
        self.fwd.sendJoinInterest('/alice/join',nonce)
        #waiting for EKEY

    def joinAccepted(self):
        pass 
        
    def joinRejected(self):
        pass

    def doSend(self, fid, name, payload):
        self.fwd.sendInterest(name,payload)
    
    def deReceive(self,data):
        self.r = self.r+1
        print("received=>",self.r)

    #Gateway
    def gateway(self):
        self.nfdc()

    #Mote
    def mote(self):
        self.nfdc()

        start = time.ticks_ms()
        self.joinInterst()
        timeout=5
        success = False 

        while timeout>0:
            print(timeout,'.',end=' ')
            if self.fwd.accepted:
                success = True 
                break 
            timeout=timeout-1
            time.sleep(1)
        stop = time.ticks_ms()
        if self.fwd.stop:
            stop = self.fwd.stop
        #192.168.1.82
        self.exp.write_n_close(start, stop, success)

        # if not self.fwd.EKEY:
        #     print("No joinInterst returned!!")
        #     return

        #self.doSend()
