import binascii
from ndn import Ndn
import time
from umqtt.robust import MQTTClient

class MQTTx: #NDN overlays over MQTT
    def __init__(self, fid, uuid="client_id", mqtt_config):

        self.fid = fid
        self.ndn = Ndn()
        self.onRecievedInterest = None
        self.onReceivedData = None
        self.mqttx = MQTTClient(uuid, mqtt_config['server'], mqtt_config['port'], mqtt_config['username'], mqtt_config['password'])
        self.mqttx.DEBUG = False 
        self.mqttx.KEEP_QOS0 = False
        self.mqttx.NO_QUEUE_DUPS = True
        self.mqttx.MSG_QUEUE_MAX = 2
        self.mqttx.set_callback(self.subscribe)

        if not self.mqttx.connect(clean_session=False):
           print("MQTT connected")
            
    def add(self,name):
        self.mqttx.subscribe(name)

    def send(self, _type, name, payload):
        if len(payload) <= 0:
            return
        self.mqttx.publish(name, payload)
        
    def subscribe(self, topic, data):
        topic = topic.decode() if isinstance(topic, (bytes)) else topic
        data = payload.decode() if isinstance(data, (bytes)) else data

        #topic == name 
        #t, l, v = self.ndn.tlv_decode(payload)
        pkt_type, f_count, f_index, p_len, n_len, chksum, name, payload = self.ndn.decode(data)
        
        if pkt_type is None:
            return 
        print(self.fid, p_len, n_len, name, payload)

        if t == Ndn.INTEREST:
            if self.onRecievedInterest:
                print("onRecievedInterest:",self.fid, p_len, n_len, name, payload)
                self.onRecievedInterest(self.fid, p_len, n_len, name, payload)
                
        elif t == Ndn.DATA:
            if self.onReceivedData:
                print("onReceivedData:",self.fid, p_len, n_len, name, payload)
                self.onReceivedData(self.fid, p_len, n_len, name, payload)
                

    def receive(self):
        self.mqttx.check_msg()