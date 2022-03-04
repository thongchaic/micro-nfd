import machine 
import dht 

class WeatherMonitoring:
    def __init__(self, fid, _pin):
        self.fid = fid 
        self.dht22 = dht.DHT22(machine.Pin(_pin))

    def send(self,_type,name,payload):
        pass 

    def handle(self):
        pass 

    def readTempHumid(self):
        temp = self.dht22.temperature()
        humid = self.dht22.humidity()
        if temp and humid:
            return temp, humid
        return None, None 
