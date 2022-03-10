import os 
import time
import machine
import network
import gc 
import esp

class WifiManager(object):
    def __init__(self,wifi_config):
        print(wifi_config)
        if wifi_config['ssid'] is None:
            return 
            
        self.ssid = wifi_config['ssid']
        self.pwd = wifi_config['password']
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.ip = None 
    
    def ip(self):
        if self.ip is None:
            return None
        return self.ip[0]
    def netmask(self):
        if self.ip is None:
            return None
        return self.ip[1]
    def gateway(self):
        if self.ip is None:
            return None
        return self.ip[2]
    def dns(self):
        if self.ip is None:
            return None
        return self.ip[3]
    
    def is_connected(self):
        return wlan.isconnected()

    def reconnect(self):
        self.do_connect()

    def do_connect(self):
        timeout = 120 #seconds 
        self.wlan.connect(self.ssid, self.pwd)
        #c = 0
        while not wlan.isconnected():
            #c = c + 1
            #print('.',end='')
            if timeout <= 0:
                print("connection failure!")
                return False
            timeout = timeout-1
            time.sleep(1)

        self.ip = wlan.ifconfig()[0]
        print("connected! ", self.ip)
        return True