import esp32 
import gc 

class ExperimentalData:
    def __init__(self, file_name):
        self.file_name = file_name
    
    def write_n_close(self,app,n,started_at, stopped_at,n_size,pl_size,pkt_size):
        self.out_file = open(self.file_name,"a")
        tf = esp32.raw_temperature()
        gc.collect()
        mem = gc.mem_free()
        print(app,str(n),str(started_at),str(stopped_at),str(n_size),str(pl_size),str(pkt_size),str(tf),str(mem),sep="\t")
        self.out_file.write(app+","+str(n)+","+str(started_at)+","+str(stopped_at)+","+str(n_size)+","+str(pl_size)+","+str(pkt_size)+","+str(tf)+","+str(mem)+"\n")
        self.out_file.close()