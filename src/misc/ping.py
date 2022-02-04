from ndn import Ndn 
import time 
import gc 
class PingApp:
    def __init__(self,fid, name):
        gc.enable()
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
        gc.collect()       
        p_len = 1
        n_len = 1
        chksum = 0xFF
        payload = 'X.'+payload.decode()
        #Response ping message
        self.onReceivedData(self.fid, p_len, n_len, chksum, name, payload)

    
