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
from lora import LoRa
from face_table import FaceTable
from routes import Routes

class Forwarder(object):
    def __init__(self,uuid,config):
        self.UUID=uuid 

        self.table = FaceTable()
        self.routes = Routes()

        self.udp = UDP(1500)
        self.udp.onRecievedInterest = onRecieveInterest
        self.udp.onReceivedData = onReceivedData
        self.table.add(self.udp.fid, self.udp)

        self.lora = LoRa(125)
        self.lora.onRecieveInterest = onRecieveInterest
        self.lora.onReceivedData = onReceivedData
        self.table.add(self.lora.fid, self.lora)

    def onRecievedInterest(self,fid,t, c, i, l,interest):
        print(fid,t, c, i, l,interest)
        #strategy & forward 
        
    def onReceivedData(self,fid,t, c, i, l, data):
        print(fid,t, c, i, l, data)

    def sendInterest(self,name,data):
        _fid = self.table.match(name)
        if _fid is None:
            self.nack(name)

    def sendData(self,name,data):
        pass 
        
    def nack(self,name):
        pass 
        
    def onReceivedNack(self):
        pass

    
