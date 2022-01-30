import os 
import time
import socket
import random
from udp import UDP
from lora import LoRa
from face_table import FaceTable
from routes import Routes
from ndn import Ndn


class Forwarder(object):
    def __init__(self,uuid, device_config, lora_parameters, app_config):

        self.stop = None 

        self.fid = 1
        self.UUID=uuid 
        self.table = FaceTable()
        self.routes = Routes()
        self.accepted = False

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

    def onRecievedInterest(self,in_face, p_len, n_len, chksum, name, payload):
        print("onRecievedInterest=>",in_face, p_len, n_len, chksum, name, payload)

        if name is None: #Unsolicited 
            return
        
        #no cs implemented

        #pit 
        if self.routes.pit(in_face,name):
            #Already in Pit  
            #print(name,"already in PIT!")
            return
        
        #fwd interest 
        if not self.routes.match(name):
            #Nack reason: routes not found
            print(name, "no routes")
            self.nack(in_face, name,'no routes')
            return

        #fw interest
        self.sendInterest(in_face,name,payload)
        
    def onReceivedData(self,in_face, p_len, n_len, chksum, name, payload):
        print("onReceivedData=>",in_face, p_len, n_len, chksum, name, payload)

    def sendInterest(self,in_face, name, interest):
        fids = self.routes.get(name) 
        for fid in fids:
            print("sendInterest:",in_face, fid, name)
            if in_face != fid:
                out_face = self.table.get(fid)
                out_face.send(Ndn.INTEREST, name, interest)
    #accepted
    def sendData(self, fid, name, data):
        out_face = self.table.get(fid)
        if out_face:
            out_face.send(Ndn.DATA, name, data)


    def onReceivedJoinInterest(self,in_face, p_len, n_len, chksum, name, payload):
        if name is None: #Unsolicited 
            return
            
        print("JoinInterest=>",in_face, p_len, n_len, chksum, name, payload)
        accepted = True 

        if accepted:
           self.sendJoinData(in_face,name,payload)
        else:
            self.nack(in_face,name,"rejected") 
    
    def onReceivedJoinData(self,fid, p_len, n_len, chksum, name, payload):
        #store EKEY 
        self.accepted=True 
        print("Accetped : ", payload)
        #app_config['EKEY'] = payload
        self.stop = time.ticks_ms()


    def sendJoinInterest(self, name, interest):
        fids = self.routes.get(name) 
        #print("fids=>",fids)
        for fid in fids:
            out_face = self.table.get(fid)
            if out_face:
                print("sendJoinInterest=>",name,interest)
                out_face.send(Ndn.JOIN_INTEREST, name, interest)

    def sendJoinData(self, fid, name, data):
        out_face = self.table.get(fid)
        if out_face:
            print("sendJoinData=>",name,data)
            out_face.send(Ndn.JOIN_DATA, name, data)

    def nack(self,fid, _type, name, reason):
        out_face = self.table.get(fid)
        if out_face:
            out_face.send(_type,name,data)  
        
    def onReceivedNack(self):
        pass

    
