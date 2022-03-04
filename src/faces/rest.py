import requests 
from ndn import Ndn 
class RESTFul:
    def __init__(self, fid, uri):
        self.URI = uri
        self.fid = fid 
        self.onRecievedInterest = None
        self.onReceivedData = None  

    def send(self,_type,name,payload):
        if _type == Ndn.DATA:
            self.receive(_type,name,payload)
            return 
        if _type == Ndn.INTEREST:
            #process and 
            pass 

        #Interest pkt received 
        
    def receive(self):
        #Data pkt received 
        pass 

    def get(self,params): #paprams format: x=1&y=2.5
        rst = requests.get(self.URI+"?"+params)
        return rst 

    def post(self,path,data):
        rst = requests.post(self.URI+path,data)
        return rst 

    def put(self):
        pass
    def delete(self, id):
        rst = requests.delete(self.URI+"/"+id)
        return rst 
    def json(self, data):
        pass 
    

    