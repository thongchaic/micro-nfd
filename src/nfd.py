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
from experiments import ExperimentalData
from ping import PingApp
from fw import Forwarder
import gc 
class MicroNFD(object):
    # 1 Gw
    # 0 Sensor
    def __init__(self):
        self.UUID = ubinascii.hexlify( machine.unique_id() ).decode()
        gc.enable()
        self.hash=uhashlib.sha256()
        
        self.exp = ExperimentalData("data.csv")
        self.fwd = Forwarder(self.UUID, device_config, lora_parameters, app_config)
       
        #ping app 
        self.ping = PingApp(2, "/alice/ping")
        self.fwd.addFaceTable(self.ping.fid, self.ping)
        

    def joinInterst(self):
        #NDN-LPWAN JoinInterest Procedure 
        nonce = str(urandom.random())
        self.fwd.sendJoinInterest('/alice/join',nonce)
        #waiting for EKEY

    def joinAccepted(self):
        pass 
        
    def joinRejected(self):
        pass

    #----------- experiments only -------------
    #Gateway
    def gateway(self):
        print("\n=====GATEWAY=====")
        self.fwd.addRoute(1,"/alice/join")
        self.fwd.addRoute(2,self.ping.get_name())

    #Mote
    def mote(self):
        print("\n=====MOTE=====")
        self.fwd.addRoute(1,"/alice/join")
        self.fwd.addRoute(1,self.ping.get_name())
        #self.fwd.addRoute(2,self.ping.get_name())

        time.sleep(2)
        gc.collect()
        print("======================BOOTSTRAP======================")
        n = 35
        n_size = len("/alice/join")
        while n > 0:
            start = time.ticks_ms()
            # self.fwd.pkt_size = 0
            # self.fwd.payload_size = 0
            self.joinInterst()
            timeout=10
            while timeout>0:
                print(timeout,'.',end=' ')
                
                if self.fwd.accepted:
                    break 
                timeout=timeout-1
                time.sleep(1)
            stop = time.ticks_ms()
            payload_size=self.fwd.payload_size
            pkt_size=self.fwd.pkt_size
            if self.fwd.stop:
                stop = self.fwd.stop

            self.exp.write_n_close("bootstrap",n,start,stop,n_size,payload_size,pkt_size)
            print('')
            n = n - 1
            time.sleep(1)

        time.sleep(3)
        gc.collect()
        print("======================DELAY======================")
        
        for x in [5,50,100,150,200,250,300]: #encode(payload + header) = pkt_size 
            n = 35
            while n > 0:
                payload = "Q"+str(x)
                self.ping.sended_at = time.ticks_ms()
                self.ping.received_at = None 
                self.ping.pkt_size = -1
                self.ping.payload_size = -1
                self.fwd.sendInterest(self.ping.fid , self.ping.get_name(), payload)
                timeout = 10
                while timeout>0:
                    print(timeout,'.',end=' ')
                    if self.ping.received_at:
                        break
                    time.sleep(1)
                    timeout=timeout-1
                n_size = len(self.ping.get_name())
                pl_size = self.ping.payload_size if self.ping.payload_size else -1
                pkt_size = self.ping.pkt_size if self.ping.pkt_size else -1
                self.exp.write_n_close('ping',n, self.ping.sended_at, self.ping.received_at,n_size, pl_size,pkt_size)
                print('')
                n=n-1
                time.sleep(1)
        print("======================GOODLUCK======================")
        
