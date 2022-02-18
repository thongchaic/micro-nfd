import requests 
from ndn import Ndn 
class RESTFul:
    def __init__(self, uri):
        self.URI = uri
        self.onRecievedInterest = None
        self.onReceivedData = None  

    
    def send(self,_type,name,payload):
        if _type == Ndn.DATA:
            self.receive(_type,name,payload)
            return 
        #Interest pkt received 
        

    def receive(self):
        #Data pkt received 
        pass 

    def get(self,params): #paprams format: x=1&y=2.5
        rst = requests.get(self.URI+"?"+params)
        return rst 

    def post(self):
        pass
    def put(self):
        pass
    def delete(self, id):
        pass
    

    