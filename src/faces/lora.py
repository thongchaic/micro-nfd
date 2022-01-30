import _thread
import time 
from machine import Pin, SoftSPI, UART
from sx127x import SX127x
from ndn import Ndn

#ESP32 TTGOv1 

class LoRa(object):
    def __init__(self, fid, device_config, lora_parameters):

        self.ndn = Ndn("LoRa")
        self.onRecievedInterest = None
        self.onReceivedData = None
        self.onReceivedJoinInterest = None 
        self.onReceivedJoinData = None 
        
        # device_spi = SPI(baudrate = 10000000, 
        #     polarity = 0, phase = 0, bits = 8, firstbit = SPI.MSB,
        #     sck = Pin(device_config['sck'], Pin.OUT, Pin.PULL_DOWN),
        #     mosi = Pin(device_config['mosi'], Pin.OUT, Pin.PULL_UP),
        #     miso = Pin(device_config['miso'], Pin.IN, Pin.PULL_UP))

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
        self.stop = False 
        self.on_send = False
        time.sleep(1)
        #self.lora.on_receive(self.on_receive)
        _thread.start_new_thread(self.daemon,())
        
    def face_id(self):
        return self.fid 
    
    def terminate(self):
        self.stop = True 

    def send(self,_type, name, payload):
        if len(payload)<=0:
            return
        self.on_send = True
        hexlify = self.ndn.encode(_type,name,payload)
        print("hexlify=>",hexlify)
        
        self.lora.println(hexlify, implicit_header=False)
        self.on_send = False
        
    def receive(self,payload=None):
        if payload is None or len(payload) < 14:
            return
        print("payload=>",payload)
        pkt_type, f_count, f_index, p_len, n_len, chksum, name, payload = self.ndn.decode(payload)
        print(pkt_type, f_count, f_index, p_len, n_len, chksum)
        if pkt_type is None:
            return 

        if f_count != (f_index+1):
            #--TODO-- 
            #--reassembly process
            return 

        print("decoded=>",pkt_type, f_count, f_index, p_len, n_len, chksum, name, payload)

        if pkt_type  == Ndn.INTEREST:
            if self.onRecievedInterest:
                self.onRecievedInterest(self.fid, p_len, n_len, chksum, name, payload)
        elif pkt_type == Ndn.DATA:
            if self.onReceivedData:
                self.onReceivedData(self.fid, p_len, n_len, chksum, name, payload)
        elif pkt_type == Ndn.JOIN_INTEREST:
            if self.onReceivedJoinInterest:
                self.onReceivedJoinInterest(self.fid, p_len, n_len, chksum, name, payload)
        elif pkt_type == Ndn.JOIN_DATA:
            if self.onReceivedJoinData:
                self.onReceivedJoinData(self.fid, p_len, n_len, chksum, name, payload)

    def on_receive(self):
        print(".",end='')

    def daemon(self):
        print("********** LoRa started **********")
        while not self.stop:
            if self.on_send:
                continue
            payload=None
            if self.lora.received_packet():
                payload = self.lora.read_payload()
                self.receive(payload)
            
    