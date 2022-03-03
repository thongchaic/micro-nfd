import machine 
import dht 

class WeatherMonitoring:
    def __init__(self, fid, _pin):
        self.fid = fid 
        self.dht22 = dht.DHT22(machine.Pin(_pin))
        
    def send(self,_type,name,payload):
        pass 
    def receive(self, _type, name, payload):
        pass 
    def readTempHumid(self):
        pass 