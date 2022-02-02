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
    def satisfied(self,name):
        if name in self.name:
            return True 
        return False 
    def send(self,_type,name,payload):
        #p_len, n_len, chksum, name, payload
        if len(payload)<=0:
            return
        # hexlify = self.ndn.encode(pkt_type,name,payload)
        # print("ping hexlify=>",hexlify)
       
        p_len = 1
        n_len = 1
        chksum = 0xFF
        #print("PingApp Received...")
        #print("send()=>onReceivedData(",self.fid, p_len, n_len, _type,name,payload,")")
        #pkt_type, f_count, f_index, p_len, n_len, chksum, name, payload = self.ndn.decode(payload)
        self.onReceivedData(self.fid, p_len, n_len, chksum, name, payload)
     
    
