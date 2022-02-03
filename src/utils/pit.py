class Pit:
    
    def __init__(self):
        print("pit init")
        self.pit = {}
    
    def add(self, fid, name):
        pirnt("pit.add:",name, fid)
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
    
    

