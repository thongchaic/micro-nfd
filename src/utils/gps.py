from machine import UART

class GPS(object):
    def __init__(port=1):
        self.gps = UART(port=1,rate=9600,bits=8,parity=None,stop=1,tx=12,rx=34)
        self.gps.init(rate,bits,parity,stop,tx,rx)
    def full_loc():
        return self.gps.read()
    def lat_lng():
        pass 
