import _thread
import time 
import socket
import random
import ndn

#----- LoRa -----
from sx127x import SX127x
from controller_esp32 import ESP32Controller
import lora_utils


class Face:

    def __init__(self,mtu):
        print("#Face init")
        self.on_Interest = None
        self.on_Data = None 
        
        self.stop = False
        self.MTU = mtu
        self.fid = self.generate_face_id()
        self.fragments = [] # in a tuble (index,length,data)
        print("Face init [, MTU:",self.MTU,", FID:",self.fid)

    def start_dgram_face(self,address):
        self.address = address
        _thread.start_new_thread(self.receive_dgram,())
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

    def generate_face_id(self):
        f = random.randrange(1,1000)
        print('#Face creating FID .. => ',f)
        return f

    def fragmentation(self):
        print("------TODO---------")

    def do_send(self,payload,address):
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
            if self.on_Interest is not None:
                #print('callback pl=>',payload[4::])
                self.on_Interest(payload[5::])
        elif t == ndn.TLV_DATA:
            print("incoming Data=>",payload)
            if self.on_Data is not None:
                self.on_Data(payload[4::])
        else:
            print('unsolicited interest/data')


    def do_send(self,payload,address):
        print("do_send")
        
    def receive_dgram(self):
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

    def receive_lora(self):
        controller = ESP32Controller()
        lora = controller.add_transceiver(SX127x(name = "LoRa"),
            pin_id_ss = ESP32Controller.PIN_ID_FOR_LORA_SS,
            pin_id_RxDone = ESP32Controller.PIN_ID_FOR_LORA_DIO0)

        while True:
            if lora.receivedPacket():
                try:
                    payload = lora.read_payload()
                    print("LoRa Payload=>",payload)
                except Exception as e:
                    print(e)

        