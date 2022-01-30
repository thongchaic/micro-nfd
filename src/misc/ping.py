class PingApp:
    def __init__(self,name):
        self.name = name 
    def get_name(self):
        return self.name
    def satisfied(self,name):
        if name in self.name:
            return True 
        return False 
    
