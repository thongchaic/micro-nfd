#      ^^
#     (oo)
#    /(__)\
#  -------------
#  < MicroNFD >
#  -------------     
#  Experimented on TTGOv1.0 ESP32 LoRa 
# import sys 
# sys.path.insert(0, 'fw')
# sys.path.insert(0, 'config')
# sys.path.insert(0, 'utils')
# sys.path.insert(0, 'faces')

from fw import Forwarder
from wifi_manager import WifiManager
from config import * 
import time 
import urandom 
import ubinascii
import machine

class MicroNFD(object):
    
    def __init__(self,config="config.py"):
        self.UUID = ubinascii.hexlify( machine.unique_id() ).decode()
        #read config 
        self.manager = WifiManager(wifi_config)
        self.manager.connect()
        self.fwd = Forwarder(self.UUID,device_config)

        #The haunting of MicroNFD's daemon 
        self.nfd.daemon()

class Experiment(object):
    # 1 Gw
    # 0 Sensor
    def __init__(self,role=0):

        
        self.UUID = ubinascii.hexlify( machine.unique_id() ).decode()
        self.manager = WifiManager(wifi_config)
        self.manager.connect()

        self.fwd = Forwarder("simulator",device_config, lora_parameters)
        self.n = 10
        self.r = 0
        self.owner = 10
            

    def nfdc(self):
        self.fwd.addRoute(1,"/alice/join")
        self.fwd.addRoute(1,"/alice/room/living/light")
        

    def joinInterst(self):
        #NDN-LPWAN JoinInterest Procedure 
        self.fwd.sendInterest('/alice/join','NONCE')

    def joinAccepted(self, data):
        print('Accepted: ',data)

        #1 pkts 
        self.doSend() 

    def joinRejected(self):
        pass

    def doSend(self):
        n=10
        while n > 0:
            n = n - 1
            if (n%2)==0:
                self.fwd.send("/alice/room/living/light","on")
            else:
                self.fwd.send("/alice/room/living/light","off")
            time.sleep(3)
    
    def deReceive(self,data):
        self.r = self.r+1
        print("received=>",self.r)

    def start(self):
        self.nfdc()
        if device_config['role']==0:
            x=10
            while x>0:
                print("x=>",x)
                self.joinInterst()
                x = x - 1
                time.sleep(3)

if __name__ == '__main__':
    sim = Experiment()
    sim.start()
