import os 
import time
#import socket
import random
import _thread
#from udp import UDP

from lora import LoRa
from face_table import FaceTable
from routes import Routes
from pit import Pit
from ndn import Ndn
#from cs import CS


class Forwarder(object):
    def __init__(self,uuid, device_config, lora_parameters, app_config, doReceive):

        self.stop = None 

        self.UUID=uuid 
        self.table = FaceTable()
        self.routes = Routes()
        self.pit = Pit()


        self.accepted = False
        self.doReceive = doReceive

        self.lora = LoRa(1, device_config, lora_parameters)
        # self.lora.onRecievedInterest = self.onRecievedInterest
        # self.lora.onReceivedData = self.onReceivedData
        self.lora.onReceivedJoinInterest = self.onReceivedJoinInterest
        self.lora.onReceivedJoinData = self.onReceivedJoinData
        self.addFaceTable(1, self.lora)

        self.i_buffer = []
        self.d_buffer = []
        

        _thread.start_new_thread(self.daemon,())

    def addRoute(self,fid,name):
        self.routes.add(fid,name)
    def addFaceTable(self, fid, obj):
        self.table.add(fid, obj)
        obj.onRecievedInterest = self.onRecievedInterest
        obj.onReceivedData = self.onReceivedData

    def forceSatisfied(self, name):
        self.pit.satisfied(name)

    def onRecievedInterest(self,in_face, p_len, n_len, chksum, name, payload):
        print("onRecievedInterest=>",in_face, p_len, n_len, chksum, name, payload)

        if name is None: #Unsolicited 
            return
        
        #no cs implemented
        #if self.cs.match()
        
        #pit 
        if self.pit.in_pit(name):
            return 
        #fwd interest 
        #self.routes.show()
        if not self.routes.match(name):
            self.nack(in_face,name,'no routes')
            return
            
        self.i_buffer.append( (in_face,name,payload) )

        
    def onReceivedData(self,in_face, p_len, n_len, chksum, name, payload):
        print("onReceivedData=>",in_face, p_len, n_len, chksum, name, payload)
        if self.pit.in_pit(name):
            self.d_buffer.append( (in_face, name, payload) )
        
    def sendData(self, in_face, name, payload):
        fids = self.pit.get(name)
        if len(fids)>0:
            self.pit.satisfied(name)
            for fid in fids:
                print("sendData:",in_face, fid, name, payload)
                out_face = self.table.get(fid)
                out_face.send(Ndn.DATA, name, payload)

    def sendInterest(self,in_face, name, interest):
        fids = self.routes.get(name) 
        if len(fids)>0:
            self.pit.add(in_face, name)
        for fid in fids:
            if in_face != fid:
                print("sendInterest:",in_face, fid, name, interest)
                out_face = self.table.get(fid)
                out_face.send(Ndn.INTEREST, name, interest)

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

    def nack(self,fid, name, reason):
        out_face = self.table.get(fid)
        if out_face:
            out_face.send(Ndn.NACK,name,reason)  
        
    def onReceivedNack(self):
        pass
    
    def daemon(self):
        while True:
            self.lora.daemon()
            if self.i_queue:
                i = self.i_queue.pop(0)
                self.sendInterest( i[0], i[1], i[2] )
            if self.d_queue:
                d = self.d_queue.pop(0)
                self.sendData( d[0],d[1],d[2] )
