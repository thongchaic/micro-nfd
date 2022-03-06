#import _thread
import time 
from machine import Pin, SoftSPI
from sx127x import SX127x
import math
from ndn import Ndn
#ESP32 TTGOv1 

class LoRa(object):
    def __init__(self, fid, device_config, lora_parameters):
        print("init...LoRa...")
        self.ndn = Ndn()
        self.onRecievedInterest = None
        self.onReceivedData = None
        self.onReceivedJoinInterest = None 
        self.onReceivedJoinData = None 

        self.buffer = {}

        device_spi = SoftSPI(baudrate = 10000000, 
        polarity = 0, phase = 0, bits = 8, firstbit = SoftSPI.MSB,
        sck = Pin(device_config['sck'], Pin.OUT, Pin.PULL_DOWN),
        mosi = Pin(device_config['mosi'], Pin.OUT, Pin.PULL_UP),
        miso = Pin(device_config['miso'], Pin.IN, Pin.PULL_UP))

        i=5
        while i > 0:
            print(i,'.',end=' ')
            time.sleep(1)
            i = i-1
        
        self.lora = SX127x(device_spi, pins=device_config, parameters=lora_parameters)
        self.fid = fid
        self.on_send = False
        
    def send(self,_type, name, payload):
       
        if len(payload)<=0:
            return
        self.on_send = True
        pkt_len = 14+(len(name)*2)+(len(payload)*2)
        if pkt_len>Ndn.MAX_PKT_LENGTH: #Do fragmentation 
            c = int(math.ceil(pkt_len/Ndn.MAX_PKT_LENGTH))
            size = int(len(payload)/c)+1
            for i in range( c ):
                frag = payload[i*size:(i+1)*size]
                hexlify = self.ndn.encode(_type,c,i,name,frag)
                self.lora.println(hexlify, implicit_header=False)
                time.sleep(0.5)
        else:
            hexlify = self.ndn.encode(_type,1,0,name,payload)
            self.lora.println(hexlify, implicit_header=False)
        self.on_send = False
        
    def receive(self):
        if self.on_send:
            return

        if not self.lora.received_packet():
            return 

        payload = self.lora.read_payload()
        if payload is None or len(payload) < 14:
            return

        pkt_type, f_count, f_index, p_len, n_len, chksum, name, payload = self.ndn.decode(payload)
        
        if pkt_type is None:
            return 

        if (f_count-1) != f_index: #more frag
            if name in self.buffer:
                self.buffer[name].append([f_index,payload])# = self.buffer[name] + payload
            else:
                self.buffer[name] = [f_index,payload]
            return
        
        if (f_count-1) == f_index: #last frag or no frag 
            if name in self.buffer:
                #payload = self.buffer[name] + payload
                if len(self.buffer[name]) != f_count: #missed some fragments 
                    self.buffer.pop(name)
                    return
                self.buffer[name].sort()
                _payload = ''
                for p in enumerate(self.buffer[name]):
                    _payload += p
                payload = _payload+payload
                self.buffer.pop(name)

        #pkt_size = 14+(len(name)*2)+(len(payload)*2)

        if pkt_type  == Ndn.INTEREST:
            if self.onRecievedInterest:
                self.onRecievedInterest(self.fid, p_len, n_len, name, payload)
        elif pkt_type == Ndn.DATA:
            if self.onReceivedData:
                self.onReceivedData(self.fid, p_len, n_len, name, payload)
        elif pkt_type == Ndn.JOIN_INTEREST:
            if self.onReceivedJoinInterest:
                self.onReceivedJoinInterest(self.fid, p_len, n_len, name, payload)
        elif pkt_type == Ndn.JOIN_DATA:
            if self.onReceivedJoinData:
                self.onReceivedJoinData(self.fid, p_len, n_len, name, payload)
