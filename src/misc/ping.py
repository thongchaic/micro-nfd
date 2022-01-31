from ndn import Ndn 
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
    def send(self,pkt_type,name,payload):
        #p_len, n_len, chksum, name, payload
        if len(payload)<=0:
            return
        hexlify = self.ndn.encode(pkt_type,name,payload)
        print("ping hexlify=>",hexlify)
        
        #pkt_type, f_count, f_index, p_len, n_len, chksum, name, payload = self.ndn.decode(payload)
        self.onReceivedData(self.fid, p_len, n_len, chksum, name, payload)
     
    
