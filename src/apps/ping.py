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

    def get_name(self):
        return self.name

    def match(self,name):
        if name in self.name:
            return True 
        return False

    def send(self,_type,name,payload):
        if len(payload)<=0:
            return
        #Process ping ==> 
        if _type == Ndn.INTEREST:
            #self.sended_at = time.ticks_ms()
            payload = str(self.sended_at) #add payload 
            #Response interest packets 
            self.onReceivedData(self.fid, p_len, n_len, chksum, name, payload)
        elif _type == Ndn.DATA:
            #Data packet received 
            self.received_at = time.ticks_ms()
            print(self.sended_at, self.received_at, payload, sep=",")
    