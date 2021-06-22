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
        self.lora.onRecievedInterest = self.onRecievedInterest
        self.lora.onReceivedData = self.onReceivedData
        self.lora.onReceivedJoinInterest = self.onReceivedJoinInterest
        self.lora.onReceivedJoinData = self.onReceivedJoinData
        self.table.add(self.fid, self.lora)

        # if device_config['role']==1:
        #     self.fid = self.fid+1
        #     self.udp = UDP()
        #     self.udp.onRecievedInterest = self.onRecievedInterest
        #     self.udp.onReceivedData = self.onReceivedData
        #     self.table.add(self.fid, self.udp)

    def addRoute(self,fid,name):
        self.routes.add(fid,name)

    def onRecievedInterest(self,in_face,f_count, f_index, p_len, n_len, chksum, name, payload):
        print("onRecievedInterest=>",in_face, f_count, f_index, p_len, n_len, chksum, name, payload)

        if name is None: #Unsolicited 
            return
        
        #no cs implemented

        #pit 
        if self.routes.pit(in_face,name):
            #Already in Pit  
            print(name,"already in PIT!")
            return
        
        #fwd interest 
        if not self.routes.match(name):
            #Nack reason: routes not found
            print(name, "no routes")
            self.nack(in_face, name,'no routes')
            return

        #fw interest
        self.sendInterest(in_face,name,payload)
        
    def onReceivedData(self,in_face,f_count, f_index, p_len, n_len, chksum, name, payload):
        print("onReceivedData=>",in_face,f_count, f_index, p_len, n_len, chksum, name, payload)

    def onReceivedJoinInterest(self,in_face,pkt_type, f_count, f_index, p_len, n_len, chksum, name, payload):
        if name is None: #Unsolicited 
            return

        if accepted:
           self.sendData(in_face,name,"accepted")
        else:
            self.nack(in_face,name,"rejected")

    def onReceivedJoinData(self,fid,pkt_type, f_count, f_index, p_len, n_len, chksum, name, payload):
        #store EKEY 
        self.EKEY=payload

    def sendInterest(self,in_face, name,interest):
        fids = self.routes.get(name)
        for fid in fids:
            print("sendInterest:",in_face, fid, name)
            if in_face != fid:
                out_face = self.table.get(fid)
                out_face.send(name,interest)          
    
    def sendData(self, in_face, name, data):
        fids = self.routes.get(name)
        for fid in fids:
            print("sendData:",in_face, fid, name)
            if in_face != fid:
                out_face = self.table.get(fid)
                out_face.send(name,data)  
        
    def nack(self,out_face, name, reason):
        out_face.send(name,reason)
        
    def onReceivedNack(self):
        pass

    
