class Fib:
    #Adjacency Matrix maybe works 
    def __init__(self):
        print("fib init")
        self.fibs = []
    
    def insertFib(self,fid,name):
        self.fibs.insert( (name,fid) )
        print("fib_inserted")
        
    def delFib(self,fid):
        for face in self.fibs:
            print(face.fid)


    def createMatrix(self):
        print("create matrix")
        
    
    