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

    def onRecievedInterest(self,in_face,t, c, i, l,interest):
        print(in_face,t, c, i, l,interest)

        #extract name 
        name = interest[32:64]

        if name is None: #Unsolicited 
            return
        
        #no cs implemented


        #pit 
        if self.routes.pit(name):
            #Already in Pit  
            return
        
        #fwd interest 
        if not self.routes.match(name):
            #Nack reason: routes not found
            self.nack(in_face, name,'no routes')
            return

        #fw interest
        self.sendInterest(name,interest)
        

    def onReceivedData(self,fid,t, c, i, l, data):
        print(fid,t, c, i, l, data)

        name = interest[0:32]
        if name is None:
            return

    def onReceivedJoinInterest(self,in_face,t, c, i, l,interest):
        #checking for registered devices
        # fids = self.routes.get(name)
        # if len(fids) > 0:
        #     face = self.table.get(fids[0])
        #     face.send("/data","accepted!")
        accepted = True 
        name = interest[32:64]
        if name is None: #Unsolicited 
            return

        if accepted:
           self.sendData(in_face,name,"accepted")
        else:
            self.nack(in_face,name,"rejected")

    def onReceivedJoinData(self,fid,t,c,i,l,name,data):
        #store EKEY 
        self.EKEY=data

    def sendInterest(self,fid, name,interest):
        fids = self.routes.get(name)
        if len(fids) > 0:
            out_face = self.table.get(fids[0])
            out_face.send(name,interest)
            face.send(name,interest)

    def sendData(self,out_face, name,data):
        #EKEY
        out_face.send(name,data) 
        
    def nack(self,out_face, name, reason):
        out_face.send(name,reason)
        
    def onReceivedNack(self):
        pass

    
