
import time 
class FaceTable:

    def __init__(self):
        
        self.faces = []
    def add_face(self,fid,face):
        self.faces.append((fid,face,time.tick_ms()))
    def rm_face(self,fid):
        for f in self.faces:
            print(fid,"==",f[0],f[1],f[2])
    def find_face(self,fid):
        print("find faces")
        for f in self.faces:
            if f[0] == fid:
                return f[1]
        return None
    
    def face_timeout(self):
        #----TODO-----
        