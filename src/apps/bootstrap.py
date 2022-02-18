
from ndn import Ndn 
class BootStrap:
    def __inti__(self):
        pass 
    def onJoinInterest(self):
        pass 
    def send(self,_type,name,payload):
        if _type == Ndn.JOIN_INTEREST:
            pass #Incoming Join Interest 
        elif _type == Ndn.JOIN_DATA:
            pass #returned join data 