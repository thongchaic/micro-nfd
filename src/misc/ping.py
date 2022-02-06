from ndn import Ndn 
import time 
class PingApp:
    def __init__(self,fid, name):
        self.fid = fid
        self.name = name 
        self.sended_at = None
        self.received_at = None 
        self.onRecievedInterest = None
        self.onReceivedData = None  

        self.pkt_size=-1
        self.payload_size=-1

        self.seed="TheQuickBrownFoxesJumpOverTheLazyDogs."
        for i in range(10):
            self.seed += "TheQuickBrownFoxesJumpOverTheLazyDogs."
        print("seed:",len(self.seed))

    def get_name(self):
        return self.name
    def match(self,name):
        if name in self.name:
            return True 
        return False
    def send(self,_type,name,payload,opt=None):
        if len(payload)<=0:
            return
        #Process ping ==> 
        p_len = 1
        n_len = 1
        chksum = 0xFF
        if payload.startswith("Q"):
            fetch_size=int(payload.replace('Q',''))
            #print("Ping resp:",payload)
            #Response ping message =>
            #generate payload 
            payload = self.seed[0:fetch_size]
            #print("Response Data:",payload)
            self.onReceivedData(self.fid, p_len, n_len, chksum, name, payload)
        else:
            self.received_at = time.ticks_ms()
            self.payload_size = len(payload)
            if opt:
                self.pkt_size=opt
            else:
                self.pkt_size=-1
            print("Data Received:", payload)
