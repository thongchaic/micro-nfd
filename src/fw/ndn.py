# import Data 
# import Interest
import random 

class Ndn:
    INTEREST = 4
    DATA = 5
    NACK = 6 
    JOIN_INTEREST = 7
    JOIN_ACCETED = 8
    JOIN_REJECTED = 9 

    def __init__(self):
        print("ndn init")
    
    def gen_fid(self):
        f = random.randrange(1,1000)
        print('#Face creating FID .. => ',f)
        return f
     
    def parse(payload=None):
        
        '''
            | parse 32 bits header 
            | t = 8-bit Types 
            | c = 4-bit Fragment Count 
            | i = 4-bit Fragment Index
            | l = 16-bit Length     
            | lat (optional)
            | lng (optional)
        '''

        if payload is None or len(payload) <= 4:
            return None, None, None, None 
        
        t, c, l, chksum1, reserved = payload[0],payload[1],payload[2:4], payload[4:6], payload[6:8]
        pkt_type = 0 
        frag_count = 0 
        frag_index = 0
        payload_len = 0
        chksum2=chksum1 #To be calculated

        if (INTEREST & t) == INTEREST:
            pkt_type = INTEREST
        elif (DATA & t) == DATA: 
            pkt_type = DATA
        
        frag_count = c & 0x0F
        frag_index = c & 0xF0
        frag_index >>= 4

        payload_len = l[0]
        payload_len <<= 8
        payload_len = payload_len | l[1]
         
        #print("-FragInfo=>",pkt_type,frag_count,frag_index,len(l),l,payload_len,bin(payload_len))
        return pkt_type, frag_count, frag_index, payload_len, reserved, chksum, (chksum1 == chksum2)
    
    def chksum(self,data):
        return 0xFFFF

    def encode(self,_type,name,payload):
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
        chksum = self.chksum(payload)
        #It does not perform fragmentation 

        f_count = 1 #Single Fragment
        f_index = 0 #Index of the Fragment 
        f_count = f_count << 4 
        opt = f_count | f_index 
        p_len = len(payload)
        n_len = len(name)

        encoded =   bytes(_type)+ \
                    bytes(opt)+ \
                    bytes(p_len)+ \
                    bytes(n_len)+ \
                    bytes(name)+ \
                    bytes(payload)

        return encoded