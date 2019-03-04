import _thread
import time 
import socket
import random

class Face:

    def __init__(self,address,mtu):
        print("#Face init")
        self.on_Interest = None
        self.on_Data = None 
        self.address = address
        self.stop = False
        self.mtu = mtu
        self.fid = self.generate_face_id()
        self.fragments = [] # in a tuble (index,length,data)
        print("Face init [address:",self.address,", MTU:",self.mtu,", FID:",self.fid)

    def start_dgram_face(self):
        #fid = 
        _thread.start_new_thread(self.start_face,())
        print("#Face dgram_face started...")

    def start_l2_face(self):
        print("-------TODO-------")

    def start_LoRa_face(self):
        print("-------TODO-------")

    def generate_face_id(self):
        f = random.randrange(1,1000)
        print('#Face generate FID .. => ',f)
        return f

    def register_face(self,t,info):
        print('#Face regis face ... ',t,info)

    def parse_face(self,face):
        pass

    def do_send(self,payload,address):
        print('....')

    def do_receive(self,payload,address):
        print('#Face receive from... ',address)

        

    def start_face(self):
        
        host = socket.getaddrinfo(self.address, 6363)[0][-1]
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(host)
        print("#Face dgram ",self.address," started!!!")
        while not self.stop:
            payload, addr = sock.recvfrom(8800)
            self.do_receive(payload,addr)

        print("#Face stoped!!")

    def stop_face(self):
        print("#Face => stoping face!!!")
        self.stop = True
        
        
    