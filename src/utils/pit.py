import time 
class Pit:
    
    def __init__(self,pit_timeout=10000):
        print("init...pit...")
        self.pit = {}
        self.ticks_sec = time.ticks_ms()
        self.pit_timeout = pit_timeout

    
    def add(self, fid, name):
        if name in self.pit:
            if fid not in self.pit[name]:
                self.pit[name].append(fid)
        else:
            self.pit[name] = [fid]

    def get(self, name):
        if self.pit[name]:
            return self.pit[name]
        return None

    def in_pit(self, name):
        if name not in self.pit:
            return False
        return True
    
    def satisfied(self, name):
        if name in self.pit:
            self.pit.pop(name)
            return True 
        return False 
    def pit_timeout(self):
        pass 
    def daemon(self):
        #check timeout 
        if (time.ticks_ms()-self.ticks_sec) > self.pit_timeout:
            self.pit_timeout()
            self.ticks_sec = time.ticks_ms()

    

