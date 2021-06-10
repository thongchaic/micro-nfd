import _thread
import time 
import socket
import random
import ndn

#----- LoRa -----
# from controller_esp32 import ESP32Controller
# import lora_utils
from config import *
from sx127x import SX127x
from machine import Pin, SPI, UART
from Ndn import NDN 

class Face:

    def __init__(self,mtu=-1):
        print("#Face init")

        self.ndn = NDN()

        self.onRecieveInterest = None
        self.onReceivedData = None 
        
        self.stop = False
        self.MTU = mtu
        self.fid = self.generate_face_id()
        self.fragments = [] # in a tuble (index,length,data)
        print("Face init [, MTU:",self.MTU,", FID:",self.fid)
        

    def get_fid(self):
        f = random.randrange(1,1000)
        print('#Face creating FID .. => ',f)
        return f

    def start_udp_face(self,address):
        self.address = address
        _thread.start_new_thread(self.receive_udp,())
        print("#Face dgram_face started...")
        return self.fid
        
    def start_l2_face(self):
        print("-------TODO-------")

    def start_LoRa_face(self):
        _thread.start_new_thread(self.receive_lora,())
        print("#LoRa Face started...")
        return self.fid

    def start_Sigfox_face(self):
        print("-------TODO-------")

    def start_mqtt_face(self):
        print("-------TODO-------")

    

    def fragmentation(self):
        print("------TODO---------")

    def do_send(self,payload,face):
        print('....')

    def reassembly(self):
        print("------TODO--------")

    def do_receive(self,payload,address):
        print('#Face receive from... ',address)
        #Assume no fragment 
        #(type, frag_len, frag_index, len, value)

        if len(payload) < 6:
            print('invalid interest/data')
            return 

        #print('pl=>',payload,' : ',payload[0])

        t,c,i,l = ndn.parse_tcilv(payload[0],payload[1],payload[2:4])
        if t == ndn.TLV_INTEREST:
            print("incoming Interest=>",payload)
            if self.onRecieveInterest is not None:
                #print('callback pl=>',payload[4::])
                self.onRecieveInterest(self.fid,payload[5::])
        elif t == ndn.TLV_DATA:
            print("incoming Data=>",payload)
            if self.onReceivedData is not None:
                self.onReceivedData(self.fid,payload[4::])
        else:
            print('unsolicited interest/data')


    def do_send(self,payload,address):
        print("do_send")
        
  
    def stop_face(self):
        print("#Face => stoping face!!!")
        self.stop = True

    def send_lora(self):
        pass 
        
