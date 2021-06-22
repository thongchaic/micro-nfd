# import utime 
import _thread
class FaceTable:

    def __init__(self):        
        self.faces = {}
        
    def add(self,fid,face):
        self.faces[fid] = face #utime.ticks_ms()
        #Timeout Faces: Find -> Remove 

    def remove(self,fid):
        return self.faces.pop(fid)
    
    def get(self,fid):
        if fid in self.faces:
            return self.faces[fid]
        return None

    def show(self):
        print(self.faces)
