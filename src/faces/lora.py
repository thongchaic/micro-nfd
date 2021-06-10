import _thread
from config import *
from machine import Pin, SPI, UART
from sx127x import SX127x
from Interest import Interest
from Data import Data 
from ndn import Ndn
#ESP32 TTGOv1 

class LoRa(object):
    def __init__(self):
        self.ndn = Ndn()
        self.onReceiveInterst = None
        self.onReceiveData = None
        device_config['mosi'], Pin.OUT, Pin.PULL_UP,
        device_config['miso'], Pin.IN, Pin.PULL_UP)
        device_spi = SPI(baudrate = 10000000, 
        polarity = 0, phase = 0, bits = 8, firstbit = SPI.MSB,
        sck = Pin(device_config['sck'], Pin.OUT, Pin.PULL_DOWN),
        mosi = Pin(device_config['mosi'], Pin.OUT, Pin.PULL_UP),
        miso = Pin(device_config['miso'], Pin.IN, Pin.PULL_UP))
        self.lora = SX127x(device_spi, pins=device_config, parameters=lora_parameters)
        self.fid = self.ndn.get_fid()
        #Haunted by Daemon
        _thread.start_new_thread(self.daemon,())

    def face_id(self):
        return self.fid 

    def send(self):
        pass

    def receive(self,payload=None):
        if payload is None and len(payload) > 5:
            return
        
        t,c,i,l = ndn.parse(payload)

        if t is None or c is None or i is None or l is None:
            return 

        if (Interest.TLV_INTEREST & t) == Interest.TLV_INTEREST:
            if self.onReceiveInterst is None:
                self.onReceiveInterst(_len,payload)
        elif (Data.TLV_DATA & t) == Data.TLV_DATA:
            if self.onReceiveData:
                self.onReceiveData(self.fid, _len ,ayload)
        
    def daemon(self):
        while not self.stop:
            if self.lora.received_packet():
                payload = self.lora.read_payload()
                self.receive(payload)
        print("LoRa face terminated..!")
    
    