import socket 
import binascii
import struct
from ndn import Ndn
class MQTTx:
    def __init__(self, mqtt_config):
        self.port = mqtt_config['port']
        self.server = mqtt_config['server']
        self.ndn = Ndn()
        self.onRecievedInterest = None
        self.onReceivedData = None


    def publish(self,topic,payload):
        pass 
    def subscribe(self, topic, payload):
        pass 
    
    def connect(self):
        self.sock = socket.socket()
        address = socket.getaddrinfo(self.server, self.port)[0][-1]
        self.sock.connect(address)
    
    def send(self, _type, name,payload):
        if _type == Ndn.INTEREST:
            self.publish(name, payload)

    def receive(self):
        res = self.sock.read(1)
        self.sock.setblocking(True)
        if res is None:
            return None 
        if res == b"":
            return None 
        if res == b"\xd0":
            return None 
        print(res)
        topic = None 
        payload = None 
        sz = self._recv_len()
        topic_len = self.sock.read(2)
        topic_len = (topic_len[0] << 8) | topic_len[1]
        topic = self.sock.read(topic_len)
        sz -= topic_len + 2
        if op & 6:
            pid = self.sock.read(2)
            pid = pid[0] << 8 | pid[1]
            sz -= 2
        payload = self.sock.read(sz)


        # if _type == Ndn.INTEREST:
        #     if self.onRecievedInterest:
        #         self.onRecievedInterest(_type, name, payload) 
        #self.subscribe(topic, payload)
        