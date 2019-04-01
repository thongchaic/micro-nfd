import os 
import time
import machine
import network
import ubinascii
import socket
import random
from machine import Pin

#----- NDN -----
from face import Face 
from fib import Fib 
from face_table import FaceTable
ft = FaceTable()

#----- LoRa -----
from sx127x import SX127x
from controller_esp32 import ESP32Controller
import lora_utils

p0      =   Pin(0, Pin.OUT)
p22     =   Pin(22, Pin.OUT)
GROUP_PASSWORD = 'micropythoN'
APNAME = None
p0.off()
p22.off()

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

UUID = ubinascii.hexlify(machine.unique_id()).decode()
EUI = lora_utils.mac2eui(UUID)
fibs = Fib()

# controller = ESP32Controller()
# lora = controller.add_transceiver(SX127x(name = "LoRa"),
#         pin_id_ss = ESP32Controller.PIN_ID_FOR_LORA_SS,
#         pin_id_RxDone = ESP32Controller.PIN_ID_FOR_LORA_DIO0)

#fibs = Fib

def init():
    
    print('------ init ap -----')
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap_ip_group = '4.'+str(random.randrange(4,254))+'.'+str(random.randrange(4,254))+'.1'
    ap.ifconfig((ap_ip_group, '255.255.255.0', ap_ip_group, '8.8.8.8'))
    #mac = ubinascii.hexlify(ap.config('mac')).decode()
    APNAME =  "NDN_"+str(EUI)
    ap.config(essid=APNAME,password=GROUP_PASSWORD) #channel=16
    print(ap.config('essid'))
    print(ap.config('channel'))
    print(ap.ifconfig())

    print('----- lora info ------')
    print('UUID: ',UUID)
    print('EUI : ',EUI)
    print("-----------------")
    p0.off()

def create_face(ssid,wifi):
    #wlan = network.WLAN(network.STA_IF)
    mac = ubinascii.hexlify(wifi[1]).decode()
    print(mac, wlan)
    #print("Connecting to ",ssid,mac)
    wlan.connect(ssid,GROUP_PASSWORD)

def find_neighbors():
    wlan.disconnect()
    nets = wlan.scan()

    selected_ssid = None

    for i,n in enumerate(nets):
        ssid = str(n[0], "utf-8", "ignore")
        mac = ubinascii.hexlify(n[1]).decode()
        dbm = int(n[3])
        print('NDN_[',i,']=>',ssid,",",mac,",",dbm," : ",n," | ",selected_ssid)

        '''
        if ssid.startswith("NDN_"):
            print('NDN_[',i,']=>',ssid,",",mac,",",dbm," : ",n)
            selected_ssid = ssid
            if dbm > -50 and dbm < -20 and selected_ssid is None:
                print("GOOD_DBM_FOUND:",selected_ssid)
                break
        '''

    '''
    if selected_ssid is None:
        if len(nets) > 0:
            do_connect( str(nets[0][0], "utf-8", "ignore") )
        else:
            find_neighbors()
    else:
        do_connect( selected_ssid )
    '''
    do_connect( "CSOffice2" )#Test

def do_connect(ssid=None):
    
    if ssid is None:
        find_neighbors()

    #print("Selected SSID:",ssid)
    #wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        #wlan.connect('PNHome2', 'st11ae58*')
        #wlan.connect(ssid, GROUP_PASSWORD)
        while not wlan.isconnected():
            print('Trying to connect PNHome2')
            #wlan.connect('CSOffice2')
            wlan.connect('PNHome2', 'st11ae58*')
            #wlan.connect(ssid)
            #wlan.connect('CACTUS4_2', 'cactus6444')
            time.sleep(2)
            pass
    
    #wlan.ifconfig(('192.168.1.17', '255.255.255.0', '192.168.1.1', '1.1.1.1')) #HOME
    #wlan.ifconfig(('192.168.6.110', '255.255.255.0', '192.168.6.254', '192.168.100.20')) #SRRU
    mac = ubinascii.hexlify(wlan.config('mac'),':').decode()
    print(wlan.ifconfig(), mac)
    p22.off()

def on_Interest(interest,fid):
    print("Incoming Interest[MAIN]=>",interest)

def on_Data(data,fid):
    print("Incoming Data[MAIN]=>",data)

def init_nfd():
    print("Start DGRAM face")
    dgram_face = Face(1500)
    dgram_face.on_Interest = on_Interest
    dgram_face.on_Data = on_Data
    
    fid = dgram_face.start_dgram_face('0.0.0.0')
    ft.add_face(fid,dgram_face)

    print("DGRAM_FID=",fid)


    lora_face = Face(255)
    lfid = lora_face.start_LoRa_face()
    ft.add_face(lfid,lora_face)
    print("LORA_FID=",lfid)

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
   
    find_neighbors()

    init_nfd()

    # lora.println("Helloworld")


    #do_connect()
    #nfd()

