import os 
import time
import socket
import random
from udp import UDP
from lora import LoRa
from face_table import FaceTable
from routes import Routes

class Forwarder(object):
    def __init__(self,uuid, device_config, lora_parameters):
        
        self.fid = 1
        self.UUID=uuid 
        self.table = FaceTable()
        self.routes = Routes()
        self.EKEY = None

        self.lora = LoRa(self.fid, device_config, lora_parameters)
        self.lora.onRecieveInterest = onRecieveInterest
        self.lora.onReceivedData = onReceivedData
        self.lora.onReceivedJoinInterest = onReceivedJoinInterest
        self.lora.onReceivedJoinData = onReceivedJoinData
        self.table.add(self.fid, self.lora)


        if device_config['role']==1:
            self.fid = self.fid+1
            self.udp = UDP()
            self.udp.onRecievedInterest = self.onRecievedInterest
            self.udp.onReceivedData = self.onReceivedData
            self.table.add(self.fid, self.udp)

    def addRoute(self,fid,name):
        self.routes.add(fid,name)

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
        
    def onReceivedData(self,in_face,f_count, f_index, p_len, n_len, chksum, name, payload):
        print(in_face,f_count, f_index, p_len, n_len, chksum, name, payload)

    def onReceivedJoinInterest(self,in_face,pkt_type, f_count, f_index, p_len, n_len, chksum, name, payload):
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

    def onReceivedJoinData(self,fid,pkt_type, f_count, f_index, p_len, n_len, chksum, name, payload):
        #store EKEY 
        self.EKEY=data

    def sendInterest(self,name,interest):
        fids = self.routes.get(name)
        if len(fids)>0:
            out_face = self.table.get(fids[0])
            out_face.send(name,interest)

    def sendData(self,out_face, name,data):
        #EKEY
        out_face.send(name,data) 
        
    def nack(self,out_face, name, reason):
        out_face.send(name,reason)
        
    def onReceivedNack(self):
        pass

    
