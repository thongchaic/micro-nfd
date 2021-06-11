  
import _thread
from ndn import Ndn 
from Interest import Interest 
from Data import Data

class UDP(object):
    def __init__(self):
        self.ndn = Ndn()
        self.stop = false
        self.onReceivedInterst = None
        self.onReceivedData = None 
        self.fid = self.ndn.get_fid()
        #daemon 
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
            if self.onReceivedInterst is None:
                self.onReceivedInterst(self.fid, t, c, i, l, payload)
        elif (Data.TLV_DATA & t) == Data.TLV_DATA:
            if self.onReceivedData:
                self.onReceivedData(self.fid, t, c, i, l, payload)

    def daemon(self):
        host = socket.getaddrinfo(self.address, 6363)[0][-1]
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(host)
        while not self.stop:
            payload, addr = sock.recvfrom(8800)
            self.receive(addr, payload)
        print("#Face stoped!!")