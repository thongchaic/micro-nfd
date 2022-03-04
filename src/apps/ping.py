from ndn import Ndn 
import time 
from crypt import Crypt
class PingApp:
    def __init__(self,fid, name, EKEY):
        self.fid = fid
        self.name = name 
        self.crypt = Crypt(EKEY)
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
            payload = self.crypt.encrypt( str(self.sended_at) ) #add payload 
            #Response interest packets 
            self.onReceivedData(self.fid, p_len, n_len, name, payload)
        elif _type == Ndn.DATA:
            #Data packet received 
            self.received_at = time.ticks_ms()
            data = self.crypt.decrypt(payload)
            print(self.sended_at, self.received_at, data, sep=",")
    