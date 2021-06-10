  
import _thread
from ndn import Ndn 
from Interest import Interest 
from Data import Data

class UDP(object):
    def __init__(self):
        this.ndn = Ndn()
        self.stop = false
        self.onReceiveInterst = None
        self.onReceiveData = None 
        _thread.start_new_thread(self.daemon,())

    def send(self,payload):
        #Pket construction 
        pass 
    
    def receive(selfj,addr=None,payload=None):

        if addr is None or payload is None:
            return 
        
        t,c,i,l = self.ndn.parse(payload)

        if t is None or c is None or i is None or l is None:
            return 
        
        if (Interest.TLV_INTEREST & t) == Interest.TLV_INTEREST:
            if self.onReceiveInterst is None:
                self.onReceiveInterst(self.fid, t, c, i, l, payload)
        elif (Data.TLV_DATA & t) == Data.TLV_DATA:
            if self.onReceiveData:
                self.onReceiveData(self.fid, t, c, i, l, payload)

    def daemon(self):
        host = socket.getaddrinfo(self.address, 6363)[0][-1]
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(host)
        print("#Face dgram ",self.address," started!!!")
        while not self.stop:
            payload, addr = sock.recvfrom(8800)
            self.receive(addr, payload)
        print("#Face stoped!!")