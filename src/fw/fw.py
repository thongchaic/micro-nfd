#from utils.cs import CS
import os 
import time
#import machine
#import network
#import ubinascii
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
    def __init__(self,uuid,device_config):
        self.UUID=uuid 

        self.table = FaceTable()
        self.routes = Routes()
        self.EKEY = None

        self.udp = UDP(1500)
        self.udp.onRecievedInterest = onRecieveInterest
        self.udp.onReceivedData = onReceivedData
        self.table.add(self.udp.fid, self.udp)

        self.lora = LoRa(device_config)
        self.lora.onRecieveInterest = onRecieveInterest
        self.lora.onReceivedData = onReceivedData
        self.lora.onReceivedJoinInterest = onReceivedJoinInterest
        self.lora.onReceivedJoinData = onReceivedJoinData
        self.table.add(self.lora.fid, self.lora)

    def onRecievedInterest(self,fid,t, c, i, l,interest):
        print(fid,t, c, i, l,interest)

        #extract name 
        name = interest[0:32]

        if name is None: #Unsolicited 
            return
        
        #no-cs 
        
        #PIT 
         if not self.routes.pit(name):
            #do noting 
            return
        #FWD 
        if not self.routes.match(name):
            #Nack reason: routes not found
            self.nack(fid, name)
            return
        
        
        #Join Interest s
        
        #Get multipath routes  
        # fids = self.routes.get(name)
        # face = self.table.get(fids[0])
        # #Forward
        # face.send(name,"data")

        self.sendData(name,data)

    def onReceivedData(self,fid,t, c, i, l, data):
        print(fid,t, c, i, l, data)

        name = interest[0:32]
        if name is None:
            return

    def onReceivedJoinInterest(self,fid,t,c,i,l,name,interest):
        #checking for registered devices
        fids = self.routes.get(name)
        face = self.table.get(fids[0])
        face.send("/data","accepted!")

    def onReceivedJoinData(self,fid,t,c,i,l,name,data):
        #store EKEY 
        self.EKEY=data

    def sendInterest(self,name,data):
        _fid = self.table.match(name)
        if _fid is None:
            self.nack(name)

    def sendData(self,name,data):

        fids = self.routes.get(name)
        face = self.table.get(fids[0])
        face.send(name,"data") 
        
    def nack(self,name):
        pass 
        
    def onReceivedNack(self):
        pass

    
