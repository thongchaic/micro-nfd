import os 
import time
import machine
import network
import ubinascii
import socket
import random
from face import Face 
from machine import Pin

p0      =   Pin(0, Pin.OUT)
p22     =   Pin(22, Pin.OUT)
GROUP_PASSWORD = 'micropythoN'
APNAME = None
p0.off()
p22.off()

def init():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap_ip_group = '4.'+str(random.randrange(4,254))+'.'+str(random.randrange(4,254))+'.1'
    ap.ifconfig((ap_ip_group, '255.255.255.0', ap_ip_group, '8.8.8.8'))
    mac = ubinascii.hexlify(ap.config('mac'),'').decode()

    APNAME =  "NDN_"+str(mac)

    ap.config(essid=APNAME,password=GROUP_PASSWORD) #channel=16
    print(ap.config('essid'))
    print(ap.config('channel'))
    print(ap.ifconfig())
    p0.off()

def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect('PNHome2', 'st11ae58*')
        #wlan.connect('science_3_2_2.4G')
        while not wlan.isconnected():
            time.sleep(2)
            print('Trying to connect PNHome2')
            pass

    wlan.ifconfig(('192.168.1.17', '255.255.255.0', '192.168.1.1', '1.1.1.1')) #HOME
    #wlan.ifconfig(('192.168.6.195', '255.255.255.0', '192.168.6.254', '192.168.100.20')) #SRRU
    mac = ubinascii.hexlify(wlan.config('mac'),':').decode()
    print(wlan.ifconfig(), mac)
    p22.off()

def to_producer(data, address,s):
    raspi = socket.getaddrinfo('192.168.1.18', 6363)[0][-1]
    print("from... ", address,' received : ', len(data), ' bytes, to ',raspi)
    s.sendto(data, raspi)
    
def to_consumer(data, address,s):
    print("from... ", address,' received : ', len(data), ' bytes')
    nfd1 = socket.getaddrinfo('4.4.4.5', 6363)[0][-1]
    s.sendto(data, nfd1)
    
def nfd():
    nfd = socket.getaddrinfo('0.0.0.0', 6363)[0][-1]
    nfd_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    nfd_sock.bind(nfd)
    print("NFD Started!!!")
    while True:
        try:
            data, address = nfd_sock.recvfrom(8800)
            #dst = socket.inet_ntop(socket.AF_INET,address)
            #print("DST=>",dst)
            
            if address[0] == '4.4.4.5':
                p0.on()
                print("###ToProducer... ",address)
                to_producer(data, address, nfd_sock)
                p0.off()
            else:
                p22.on()
                print("***ToConsumer... ",address)
                to_consumer(data, address, nfd_sock)
                p22.off()
            
        except:
            print("interupted ... ")
            break

if __name__ == '__main__':
    p0.on()
    p22.on()
    init()
    do_connect()
    #nfd()

