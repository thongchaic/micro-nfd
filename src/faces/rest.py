import requests 
from ndn import Ndn 
class RESTFul:
    def __init__(self):
        pass 
    
    def send(self,_type,name,payload):
        if _type == Ndn.DATA:
            self.receive(_type,name,payload)
            return 
        #Interest pkt received 
        
    def receive(self):
        #Data pkt received 

    def get(self,data):
        pass
    def post(self):
        pass
    def put(self):
        pass
    def delete(self, id):
        pass 
         
    