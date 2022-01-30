import esp32 
import gc 

class ExperimentalData:
    def __init__(self, file_name):
        self.file_name = file_name
    
    def write_n_close(self,n, started_at, stopped_at, success):
        self.out_file = open(self.file_name,"a")
        tf = esp32.raw_temperature()
        gc.collect()
        mem = gc.mem_free()
        print("\n"+str(started_at)+","+str(stopped_at)+","+str(success)+","+str(tf)+","+str(mem))
        self.out_file.write(str(n)+","+str(started_at)+","+str(stopped_at)+","+str(success)+","+str(tf)+","+str(mem)+"\n")
        self.out_file.close()