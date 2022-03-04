from ndn import Ndn 
import machine
from crypt import Crypt

class PM25DustMonitoring: #PMS3003 
    def __init__(self,fid):

        self.fid = fid
        self.onReceivedJoinInterest = None 
        self.onReceivedJoinData = None 

        self.pms = machine.UART(2,9600)
        self.pms.init(9600,bits=8,parity=None,stop=1)
        

    def send(self,_type,name,payload):
        if _type == Ndn.INTEREST:
            #process 
            pm25, pm10 = self.readPM3003s()
            if pm25 and pm10:
                payload = '{"pm25":'+str(pm25)+', "pm10":'+str(pm10)+'}'
            
            p_len = len(payload)
            n_len = len(name)

            if self.onReceivedData: #return NDN Data  
                self.onReceivedData(self.fid, p_len, n_len, name, payload)

    def receive(self,_type,name,payload):
        pass

    def calc_pms(self,x,y):
        pm25 = x
        pm25 <<= 8
        pm25 = pm25 | y
        return pm25

    def readPM3003s(self):
        try:
            raw = self.pms.read(42)
            for i, x in enumerate(raw):
                if i+9 < len(raw)-1 and x == 66 and raw[i+1] == 77:
                    pm25 = self.calc_pms(raw[i+6],raw[i+7])
                    pm10 = self.calc_pms(raw[i+8],raw[i+9])
                    return pm25, pm10
        except:
            return None, None
        return None, None

