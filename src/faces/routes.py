
class Routes(object):
    def __init__(self):
        self.routes={}
        
    def add(self,fid,name):
        if name in self.routes:
            if fid not in self.routes[name]:
                self.routes[namme].push(fid)
        else:
            self.routes[namme] = [fid]
    
    def remove(self,name):
        self.routes.pop(name)

    def get(self,name):
        return self.routes[name]

    def match(self,fid,name):
        if self.routes[name]:
            return True
        return False

    def pit(self,fid,name):
        if self.routes[name]:
            if fid not in self.routes[name]:
                self.routes[namme].push(fid)
            return True
        return False