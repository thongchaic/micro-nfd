#import time 
class CS:
    
    def __init__(self):
        self.data = {}
    
    def add_to_cs(self,name,payload):
        self.data[name] = payload

    def fetch(self,name):
        if self.data.has_key(name):
            return self.data[name]
        return None 
    def remove(self):
        if self.data.has_key(name):
            del self.data[name]
            return True
        return False 