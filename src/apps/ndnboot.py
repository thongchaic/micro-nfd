
from ndn import Ndn 
class NDNBootstrap:
    def __inti__(self, fid, app_config):
        self.app_config = app_config
        self.fid = fid
        self.onReceivedJoinInterest = None 
        self.onReceivedJoinData = None 


    def send(self,_type,name,payload):
        if _type == Ndn.JOIN_INTEREST:
            pass #Incoming Join Interest 
        elif _type == Ndn.JOIN_DATA:
            pass #returned join data 