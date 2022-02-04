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
# from wifi_manager import WifiManager
from config import * 
from experiments import ExperimentalData
from ping import PingApp
from fw import Forwarder

class MicroNFD(object):
    # 1 Gw
    # 0 Sensor
    def __init__(self):
        self.UUID = ubinascii.hexlify( machine.unique_id() ).decode()
        # self.manager = WifiManager(wifi_config)
        # self.manager.connect()
        

        self.exp = ExperimentalData("data.csv")
        self.fwd = Forwarder(self.UUID, device_config, lora_parameters, app_config, 
                            self.doReceive)
       
        #ping app 
        self.ping = PingApp(2, "/alice/ping")
        self.fwd.addFaceTable(self.ping.fid, self.ping)
        
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

    # def doSend(self, in_face,  name, payload):
    #     self.fwd.sendInterest(in_face, name,payload)
    
    #App Received 
    def doReceive(self,in_face, p_len, n_len, chksum, name, payload):
        print("nfd.receiced:", in_face, p_len, n_len, chksum, name, payload)
        #Ping App : GW   
        if self.ping.match(name):
           #self.ping.receiced(name, payload)
           #Response 
           time.sleep(2)
           self.fwd.sendData(name, 'X.'+payload.decode())
           #
           #self.doSend(self.ping.fid , self.ping.get_name(), 'X.'+payload.decode())
        #Other App .... 

    #----------- experiments only -------------
    #Gateway
    def gateway(self):
        self.fwd.addRoute(1,"/alice/join")
        self.fwd.addRoute(2,self.ping.get_name())

    #Mote
    def mote(self):
        self.fwd.addRoute(1,"/alice/join")
        self.fwd.addRoute(1,self.ping.get_name())
        #self.fwd.addRoute(2,self.ping.get_name())

        time.sleep(2)
        while True:
            payload = 'Y'+str(urandom.random())
            #self.doSend( self.ping.fid , self.ping.get_name(), payload )
            self.fwd.sendInterest(self.ping.fid , self.ping.get_name(), payload)
            time.sleep(15)

        # n = 40
        # while n > 0:
        #     start = time.ticks_ms()
        #     self.joinInterst()
        #     timeout=3
        #     success = False 

        #     while timeout>0:
        #         print(timeout,'.',end=' ')
        #         if self.fwd.accepted:
        #             success = True 
        #             break 
        #         timeout=timeout-1
        #         time.sleep(1)
        #     stop = time.ticks_ms()
        #     if self.fwd.stop:
        #         stop = self.fwd.stop
        #     self.exp.write_n_close(n, start, stop, success)
        #     n = n - 1
        #     time.sleep(2)

        # n = 40 
        # while n > 0:
        #     payload = str(urandom.random())
        #     self.ping.sended_at = time.ticks_ms()
        #     self.doSend( self.ping.get_name(), payload )
            
        #     n = n - 1 
        #     time.sleep(2)

        # if not self.fwd.EKEY:
        #     print("No joinInterst returned!!")
        #     return

        #self.doSend()
