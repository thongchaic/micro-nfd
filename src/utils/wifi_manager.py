# import os 
# import time
# import machine
import network
import time
import gc 
import esp

class WifiManager(object):
    def __init__(self,wifi_config):
        self.ssid = ssid
        self.pwd = pwd
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

    def do_connect(self):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)

        if wlan.isconnected():
            self.ip = wlan.ifconfig()
            return True

        wlan.connect(self.ssid, self.pwd)
        c = 0
        while not wlan.isconnected():
            time.sleep(1)
            c = c + 1
            if c > 300:
                return False
        self.ip = wlan.ifconfig()[0]
        return True