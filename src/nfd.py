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

class MicroNFD(object):
    def __init__(self,config="config.py"):
        self.UUID = ubinascii.hexlify( machine.unique_id() ).decode()
        #read config 
        # self.manager = WifiManager(wifi_config)
        # self.manager.connect()
        # self.fwd = Forwarder(self.UUID,device_config)
        #The haunting of MicroNFD's daemon 
        # self.nfd.daemon()

class Nfd(object):
    # 1 Gw
    # 0 Sensor
    def __init__(self,role=0):
        self.UUID = ubinascii.hexlify( machine.unique_id() ).decode()
        # self.manager = WifiManager(wifi_config)
        # self.manager.connect()
        self.fwd = Forwarder(self.UUID, device_config, lora_parameters)
        self.n = 10
        self.r = 0

    def nfdc(self):
        self.fwd.addRoute(1,"/alice/join")
        self.fwd.addRoute(1,"/alice/light/status")

    def joinInterst(self):
        #NDN-LPWAN JoinInterest Procedure 
        nonce = str(urandom.random())

        self.fwd.sendJoinInterest('/alice/join', 'hi')
        #waiting for EKEY
        
    def joinRejected(self):
        pass

    def doSend(self):
        n=10
        while n > 0:
            if (n%2)==0:
                self.fwd.sendData(1,"/alice/light/status","on")
            else:
                self.fwd.sendData(1,"/alice/light/status","off")
            n = n - 1
            time.sleep(3)
    
    def deReceive(self,data):
        self.r = self.r+1
        print("received=>",self.r)

    #Gateway
    def gateway(self):
        self.nfdc()

    #Mote
    def mote(self):
        self.nfdc()

        tries = 0
        while tries<5:
            self.joinInterst()
            tries = tries+1
            delay=10
            while delay>0:
                print(delay,'.',end=' ')
                if self.fwd.EKEY:
                    delay=0
                delay=delay-1
                time.sleep(1)
            print("retry..",tries)
            time.sleep(3)

        if not self.fwd.EKEY:
            print("No joinInterst returned!!")
            return

        self.doSend()
