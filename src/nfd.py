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
from ping import PingApp

class MicroNFD(object):
    # 1 Gw
    # 0 Sensor
    def __init__(self,role=0):
        self.UUID = ubinascii.hexlify( machine.unique_id() ).decode()
        # self.manager = WifiManager(wifi_config)
        # self.manager.connect()
        

        self.exp = ExperimentalData("data.csv")
        self.fwd = Forwarder(self.UUID, device_config, lora_parameters, app_config, 
                            self.doReceive)
       

        #ping app 
        self.ping = PingApp("/alice/ping")
        
    # def nfdc(self):
    #     #Easy to manage partial name  

    #     self.fwd.addRoute(1,"/alice/join")
    #     #self.fwd.addRoute(1,"/alice/light/status")

        

    def joinInterst(self):
        #NDN-LPWAN JoinInterest Procedure 
        nonce = str(urandom.random())
        self.fwd.sendJoinInterest('/alice/join',nonce)
        #waiting for EKEY

    def joinAccepted(self):
        pass 
        
    def joinRejected(self):
        pass

    def doSend(self, name, payload):
        self.fwd.sendInterest(name,payload)
    
    def doReceive(self,in_face, p_len, n_len, chksum, name, payload):
        print(in_face, p_len, n_len, chksum, name, payload)

        #Ping App 
        if self.ping.satisfied(name):
            print("Ping Data Returned")
        #Other App .... 

    #----------- experiments only -------------
    #Gateway
    def gateway(self):
        self.fwd.addRoute(1,"/alice/join")
        #ping app name 
        self.fwd.addRoute(2,self.ping.get_name())

    #Mote
    def mote(self):
        self.fwd.addRoute(1,"/alice/join")


        n = 40
        while n > 0:
            start = time.ticks_ms()
            self.joinInterst()
            timeout=3
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
            self.exp.write_n_close(n, start, stop, success)
            n = n - 1
            time.sleep(2)

        n = 40 
        while n > 0:
            payload = str(urandom.random())
            self.doSend( self.ping.get_name(), payload )
            n = n - 1 

        # if not self.fwd.EKEY:
        #     print("No joinInterst returned!!")
        #     return

        #self.doSend()
