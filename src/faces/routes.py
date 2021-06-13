
class Routes(object):
    def __init__(self):
        self.routes={}
        pass
    def add(self,fid,name):
        if name in self.routes:
            self.routes[namme].push(fid)
        else:
            self.routes[namme] = [fid]
    def remove(self,name):
        pass
    def get(self,name):
        return self.routes[name]
    def match(self,name):
        if self.routes[name]:
            return True
        return False 