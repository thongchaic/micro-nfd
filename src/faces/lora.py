#import _thread
import time 
from machine import Pin, SoftSPI, UART
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

        i=3
        while i > 0:
            print(i,'.',end=' ')
            time.sleep(1)
            i = i-1

        self.lora = SX127x(device_spi, pins=device_config, parameters=lora_parameters)
        self.fid = fid
        self.stop = False 
        self.on_send = False
        time.sleep(1)
        
    def face_id(self):
        return self.fid 
    
    def terminate(self):
        self.stop = True 

    def send(self,_type, name, payload,opt=None):
       
        if len(payload)<=0:
            return
        self.on_send = True

        pkt_len = 14+(len(name)*2)+(len(payload)*2)
        #print("pkt_len:",pkt_len)
        if pkt_len>Ndn.MAX_PKT_LENGTH:
            #fullhex = self.ndn.encode(_type,1,0,name,payload)
            #print("full_pkt(",len(fullhex),",",len(payload),"):",payload)
            c = int(math.ceil(pkt_len/Ndn.MAX_PKT_LENGTH))
            size = int(len(payload)/c)+1
            for i in range( c ):
                frag = payload[i*size:(i+1)*size]
                hexlify = self.ndn.encode(_type,c,i,name,frag)
                #print("frag:",_type,c,i,name,frag)
                #print("frag_hex(",len(hexlify),"):",hexlify)
                self.lora.println(hexlify, implicit_header=False)
                time.sleep(0.5)
        else:
            hexlify = self.ndn.encode(_type,1,0,name,payload)
            #print("No frag:",name,payload,len(hexlify))
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
        #print("raw:",payload)

        pkt_type, f_count, f_index, p_len, n_len, chksum, name, payload = self.ndn.decode(payload)
        #print(pkt_type, f_count, f_index, p_len, n_len, chksum,name,payload)
        
        if pkt_type is None:
            return 

        if (f_count-1) != f_index: #more frag
            if name in self.buffer:
                self.buffer[name] = self.buffer[name] + payload
            else:
                self.buffer[name] = payload
            return

        #pkt_size=len(payload)
        
        if (f_count-1) == f_index: #last frag or no frag 
            if name in self.buffer:
                payload = self.buffer[name] + payload
                self.buffer.pop(name)

        #print("full_pl:",pkt_size,payload)
        pkt_size = 14+(len(name)*2)+(len(payload)*2)

        #print("lora.decoded=>",pkt_type, f_count, f_index, p_len, n_len, pkt_size, name, payload)
        if pkt_type  == Ndn.INTEREST:
            if self.onRecievedInterest:
                self.onRecievedInterest(self.fid, p_len, n_len, pkt_size, name, payload)
        elif pkt_type == Ndn.DATA:
            if self.onReceivedData:
                self.onReceivedData(self.fid, p_len, n_len, pkt_size, name, payload)
        elif pkt_type == Ndn.JOIN_INTEREST:
            if self.onReceivedJoinInterest:
                self.onReceivedJoinInterest(self.fid, p_len, n_len, pkt_size, name, payload)
        elif pkt_type == Ndn.JOIN_DATA:
            if self.onReceivedJoinData:
                self.onReceivedJoinData(self.fid, p_len, n_len, pkt_size, name, payload)

    # def daemon(self):
    #     if self.on_send:
    #         return 
    #     payload=None
    #     if self.lora.received_packet():
    #         payload = self.lora.read_payload()
    #         if payload is None or len(payload) < 14:
    #             return
    #         print("raw:",payload)
    #         pkt_type, f_count, f_index, p_len, n_len, chksum, name, payload = self.ndn.decode(payload)
    #         if pkt_type is None:
    #             return 
    #         print("lora.decoded=>",pkt_type, f_count, f_index, p_len, n_len, chksum, name, payload)

    #         #self.receive(payload)
