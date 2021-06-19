import time 
import _thread
class FaceTable:

    def __init__(self):        
        self.faces = []
        
    def add(self,fid,face):
        self.faces.append({ fid:( face, time.time()) })
    
    def remove(self,fid):
        #for f in self.faces:
        #    print(fid,"==",f[0],f[1],f[2])
        return self.faces.pop(fid)
    
    def find(self,fid):
        # print("find faces")
        # for f in self.faces:
        #     if f[0] == fid:
        #         return f[1]
        return self.faces[fid]
    
    def face_timeout(self):
        pass 
        #----TODO-----

