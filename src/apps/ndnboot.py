
from ndn import Ndn
import json 
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
            data = json.load(payload)
            self.app_config['EKEY'] = data['EKEY']
