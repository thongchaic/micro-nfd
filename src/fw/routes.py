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

    def match(self, name):
        if name not in self.routes:
            return False
        return True
