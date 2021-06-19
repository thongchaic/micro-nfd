import socket
from ndn import Ndn
#from Interest import Interest 
#from Data import Data
import thread

class UDP(object):
    def __init__(self):
        self.ndn = Ndn()
        self.stop = False
        self.onRecievedInterest = None
        self.onReceivedData = None 
        self.fid = self.ndn.fid()
        #daemon 
        thread.start_new_thread(self.daemon,())

    def send(self,payload):
        pass
        
    def receive(selfj,addr=None,payload=None):

        if addr is None or payload is None:
            return 
        
        pkt_type, f_count, f_index, p_len, n_len, chksum, name, payload = self.ndn.decode(payload)

        if pkt_type is None:
            return
        
        if (Ndn.TLV_INTEREST & t) == Ndn.TLV_INTEREST:
            if self.onRecievedInterest is None:
                self.onRecievedInterest(self.fid, pkt_type, f_count, f_index, p_len, n_len, chksum, name, payload)
        elif (Ndn.TLV_DATA & t) == Ndn.TLV_DATA:
            if self.onReceivedData:
                self.onReceivedData(self.fid, pkt_type, f_count, f_index, p_len, n_len, chksum, name, payload)

    def daemon(self):
        print("UDP started")
        host = socket.getaddrinfo('0.0.0.0', 6363)[0][-1]
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(host)
        while not self.stop:
            payload, addr = sock.recvfrom(8800)
            self.receive(addr, payload)
        print("#Face stoped!!")