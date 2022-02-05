class Pit:
    
    def __init__(self):
        print("init...pit...")
        self.pit = {}
    
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
    def daemon(self):
        #check timeout 
        pass 
    
    

