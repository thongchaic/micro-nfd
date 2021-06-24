import esp
import esp32
import time
import urandom
from config import *
from machine import Pin, SPI, UART
from sx127x import SX127x
esp.osdebug(None)
import gc 
gc.enable()
# MAC=c44f336ab725
# EUI=c64f33fffe6ab725

#T_BEAM_V10(https://github.com/Xinyuan-LilyGO/LilyGO-T-Beam/blob/master/src/board_def.h)
#define GPS_RX_PIN 34
#define GPS_TX_PIN 12
#define BUTTON_PIN 38
#define BUTTON_PIN_MASK GPIO_SEL_38

#define LORA_SCK        5
#define LORA_MISO       19
#define LORA_MOSI       27
#define LORA_SS         18
#define LORA_DI0        26
#define LORA_RST        23
#define LORA_DIO1       33
#define LORA_BUSY       32

class SRRULoRa:
    def __init__(self,_id,ssid,ssid_pass):
        
        print("init....",device_config)
        print(lora_parameters)
        self.ssid=ssid
        self.ssid_pass = ssid_pass

        self.gps = UART(1)
        self.gps.init(9600,bits=8,parity=None,stop=1,tx=12,rx=34)

        # print("SPI==>")
        # print(0,0,8,SPI.MSB,device_config['sck'], Pin.OUT, Pin.PULL_DOWN,
        # device_config['mosi'], Pin.OUT, Pin.PULL_UP,
        # device_config['miso'], Pin.IN, Pin.PULL_UP)

        # print(device_config)
        # print(lora_parameters)

        device_spi = SPI(baudrate = 10000000, 
        polarity = 0, phase = 0, bits = 8, firstbit = SPI.MSB,
        sck = Pin(device_config['sck'], Pin.OUT, Pin.PULL_DOWN),
        mosi = Pin(device_config['mosi'], Pin.OUT, Pin.PULL_UP),
        miso = Pin(device_config['miso'], Pin.IN, Pin.PULL_UP))
        
      
        self.lora = SX127x(device_spi, pins=device_config, parameters=lora_parameters)

    def do_connect(self):
        import network
        wlan=network.WLAN(network.STA_IF)
        wlan.active(True)

        if wlan.isconnected():
            print("connected... ",wlan.ifconfig())
            return True
        
        wlan.connect(self.ssid,self.ssid_pass)
        t0 = time.ticks_ms()
        while not wlan.isconnected():
            tn = time.ticks_diff(time.ticks_ms(), t0)
            print(t0,time.ticks_ms(), tn)
            time.sleep(1)
            if tn > (1000*10):
                print("connection failed....")
                return False

        print(wlan.ifconfig())
        return True
        
    def read_gps(self):
        gps = self.gps.read() 



        return gps if gps else None

    def infinity_life(self):
        import machine

        c = 0

        self.do_connect()
        gps = self.read_gps()
        print(gps)
        print('-----------')
        #self.lora.println("hello")

        while True:
        #    #self.do_connect()

        #   #gps = self.read_gps()
        #    #print("---->",gc.mem_free(),"<----")
        #    #print(gps)
        #
            payload = "0410ffff06052f68656c6c6f776f726c64"
            print("Sending=>",payload)
            self.lora.println(payload, implicit_header=False) #implicit_header=True = No data transmited 
        #    if self.lora.received_packet():
        #        payload = self.lora.read_payload()
        #        print("payload=>",payload)
            #self.lora.dump_registers()
            c = c + 1
        #    print('.')
            time.sleep(5)
        #    print(".",end="")
        #    #if gc.mem_free() < 60000:
        #    #    machine.reset()
        #    #else:
        #    #    print("collect..")
        #    #    gc.collect()

# if __name__ == '__main__':
#     #str(urandom.getrandbits(30))
#     iot = SRRULoRa("","PNHome2","st11ae58*")
#     iot.infinity_life()
#     print("---")

