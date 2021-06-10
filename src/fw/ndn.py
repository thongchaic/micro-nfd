import Data 
import Interest
import random 

class Ndn:
    def __init__(self):
        print("ndn init")

   def get_fid(self):
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
    
    t,ci,l = payload[0],payload[1],payload[2:4]
    pkt_type = 0
    frag_count = 0 
    frag_index = 0
    payload_len = 0

    if (Interest.TLV_INTEREST & t) == Interest.TLV_INTEREST:
        pkt_type = Interest.TLV_INTEREST
    elif (Data.TLV_DATA & t) == Data.TLV_DATA:
        pkt_type = Data.TLV_DATA

    frag_count = ci & 0x0F
    frag_index = ci & 0xF0 
    frag_index >>= 4

    payload_len = l[0]
    payload_len <<= 8
    payload_len = payload_len | l[1]
    
    #print("-FragInfo=>",pkt_type,frag_count,frag_index,len(l),l,payload_len,bin(payload_len))
    return pkt_type, frag_count, frag_index, payload_len