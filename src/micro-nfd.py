import os 
import time
import machine
import network
import ubinascii
import socket
import random

#----- NDN -----
from fw import Forwarder 
UUID = ubinascii.hexlify(machine.unique_id()).decode()

#EUI = lora_utils.mac2eui(UUID)
class MicroNFD(object):
    def __init__(self,config="config.py"):
        #read config 
        self.daemon=True


        
        fwd = Forwarder(self.UUID,self.config)
        if(self.config['daemon']):
            fwd.init_daemon()
        else:
            fwd.start()
            

        # print(UIID)
        # print("Start UDP face")

        # udp = Face(1500)
        # udp.on_Interest = on_Interest
        # udp.on_Data = on_Data
        # fid = udp.start_udp_face('0.0.0.0')

        # lora_face = Face(125)
        # lfid = lora_face.start_LoRa_face()
    
 
    
if __name__ == '__main__':
    micro_nfd = MicroNFD()


# def to_producer(data, address,s):
#     raspi = socket.getaddrinfo('192.168.1.18', 6363)[0][-1]
#     print("from... ", address,' received : ', len(data), ' bytes, to ',raspi)
#     s.sendto(data, raspi)
    
# def to_consumer(data, address,s):
#     print("from... ", address,' received : ', len(data), ' bytes')
#     nfd1 = socket.getaddrinfo('4.4.4.5', 6363)[0][-1]
#     s.sendto(data, nfd1)
    
# def nfd():
#     nfd = socket.getaddrinfo('0.0.0.0', 6363)[0][-1]
#     nfd_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     nfd_sock.bind(nfd)
#     print("NFD Started!!!")
#     while True:
#         try:
#             data, address = nfd_sock.recvfrom(8800)
#             #dst = socket.inet_ntop(socket.AF_INET,address)
#             #print("DST=>",dst)
            
#             if address[0] == '4.4.4.5':
#                 p0.on()
#                 print("###ToProducer... ",address)
#                 to_producer(data, address, nfd_sock)
#                 p0.off()
#             else:
#                 p22.on()
#                 print("***ToConsumer... ",address)
#                 to_consumer(data, address, nfd_sock)
#                 p22.off()
            
#         except:
#             print("interupted ... ")
#             break

