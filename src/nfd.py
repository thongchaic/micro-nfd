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
import uhashlib
# from wifi_manager import WifiManager
from config import * 
#from experiments import ExperimentalData
from ping import PingApp
from fw import Forwarder
import gc

from ping import PingApp
from ndnboot import NDNBootstrap

class MicroNFD(object):

    def __init__(self):
        self.UUID = ubinascii.hexlify( machine.unique_id() ).decode()
        gc.enable()
        self.hash=uhashlib.sha256()

        self.mode = app_config['mode']
        
        #self.exp = ExperimentalData("data.csv")
        self.fwd = Forwarder(self.UUID, device_config, lora_parameters, app_config)



    def mote(self):
        #bootstrap app 
        self.boot = NDNBootstrap(3,app_config)
        self.fwd.addFaceTable(self.boot.fid, self.boot)
       
        #ping app 
        self.ping = PingApp(2, "/alice/ping")
        self.fwd.addFaceTable(self.ping.fid, self.ping)

        # while True:
        #     #app interval 
        #     time.sleep(60)
    
    def deepsleep(self):
        pass 