INTEREST = 4#i=ord('\x01')
from ndn import Ndn 

class Interest(object):
    def __init__(self):
        pass
    def encode(self,name,payload):
        #Header + Payload 
        '''
            | parse 32 bits header 
            | t = 8-bit Types 
            | c = 4-bit Fragment Count 
            | i = 4-bit Fragment Index
            | l = 16-bit Length     
            | lat (optional)
            | lng (optional)
        '''
        chksum = 0
        t = INTEREST
        #does not perform fragmentation 
        c = 1
        i = 0
        c = c << 4
        opt = c | i 
        p_len = len(payload)
        n_len = len(name)

        encoded =   bytes(t)+ \
                    bytes(opt)+ \
                    bytes(p_len)+ \
                    bytes(n_len)+ \
                    bytes(name)+ \
                    bytes(payload)

        return encoded

    def toString(self):
        pass
    
    
