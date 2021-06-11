#      ^^
#     (oo)
#    /(__)\
#  -------------
#  < MicroNFD∞ >
#  -------------      
from fw import Forwarder
from wifi-manger import WifiManager
from config import * 
import time 
import urandom 

UUID = ubinascii.hexlify(machine.unique_id()).decode()
#EUI = lora_utils.mac2eui(UUID)

class MicroNFD(object):
    def __init__(self,config="config.py"):
        #read config 
        self.manager = WifiManager(wifi_config)
        self.manager.connect()
        self.fwd = Forwarder(self.UUID,self.config)
        #The huanting of MicroNFD's daemon 
        self.nfd.daemon()

class Simulator(object):
    # 0 Gw
    # 1 Sensor 
    def __init__(self,role=0):

        self.manager = WifiManager(wifi_config)
        self.manager.connect()
        self.fwd = Forwarder(self.UUID,self.config)

        self.n = 10
        self.r = 0
        self.owner = 10
        self.nonce = urandom.random()
    
    def joinInterst(self):
        #NDN-LPWAN JoinInterest Procedure 
        self.fwd.send('/alice/join',self.nonce)

         
    def joinAccepted(self, data):
        self.fwd.send("/alice/KEY","sig/")

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
    
    def start(self):
        pass 


if __name__ == '__main__':
    sim = Simulator()
    sim.start(0)
