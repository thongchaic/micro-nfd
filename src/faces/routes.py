class Routes(object):
    def __init__(self):
        self.routes={}
                
    def add(self, fid, name):
        if name in self.routes:
            if fid not in self.routes[name]:
                self.routes[name].append(fid)
        else:
            self.routes[name] = [fid]
        self.show()
        
    def show(self):
        print(self.routes)

    def remove(self, name):
        if name in self.routes:
            self.routes.pop(name)

    def get(self,name):
        if name in self.routes:
            return self.routes[name]
        return None 

    def match(self, fid, name):
        if name not in self.routes:
            return False
        return True

    def pit(self, fid, name):
        if name not in self.routes:
            self.add(fid,name)
            return False

        if fid not in self.routes[name]:
            self.routes[name].append(fid)
            return True  

        return True
    
    def satisfied(self, fid, name):#Deprecated
        if name not in self.routes:
            return
        if fid not in self.routes[name]:
            return
        self.routes[name].pop(fid)
        if len(routes[name]) <= 0:
            self.remove(name)
        