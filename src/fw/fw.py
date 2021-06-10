from utils.cs import CS
import os 
import time
import machine
import network
import ubinascii
import socket
import random
#----- NDN -----
# from face import Face 
# from fib import Fib 
# from face_table import FaceTable
from udp import UDP

class Forwarder(object):
    def __init__(self,uuid,config):
        self.UUID=uuid 

        udp = UDP(1500)
        udp.onRecieveInterest = onRecieveInterest
        udp.onReceivedData = onReceivedData
        fid = udp.start_udp_face('0.0.0.0')

        lora = Face(125)
        lora.onRecieveInterest = onRecieveInterest
        lora.onReceivedData = onReceivedData

        lfid = lora_face.start_LoRa_face()


    def onRecieveInterest(self,interest):
        print(interest)
        
    def onReceivedData(self):
        pass
    def onReceivedNack(self):
        pass
