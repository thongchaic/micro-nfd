class Fib:
    
    def __init__(self):
        print("fib init")
        self.fibs = []
    
    def insertFib(self,face,name):
        self.fibs.insert( (face,name) )
        print("fib_inserted")

    
    def delFib(self,fid):
        for face in self.fibs:
            print(face.fid)


    