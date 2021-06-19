import random 
import binascii


class Ndn:
    INTEREST = 4
    DATA = 5
    NACK = 6 
    JOIN_INTEREST = 7
    JOIN_ACCETED = 8
    JOIN_REJECTED = 9 


    def __init__(self):
        print("ndn init")
    
    def fid(self):
        f = random.randrange(1,1000)
        return f
     
    def decode(self, raw="0410ffff05062f68656c6c6f776f726c64"):
        '''
            | parse 32 bits header 
            | t = 8-bit Types 
            | c = 4-bit Fragment Count 
            | i = 4-bit Fragment Index
            | l = 16-bit Length     
            | lat (optional)
            | lng (optional)
        '''
        if raw is None or len(raw) <= 14:
            return None, None, None, None 
     
        pkt_type = int(raw[0:2],16)
        # pkt_type = 0

        # if (Ndn.INTEREST & t) == Ndn.INTEREST:
        #     pkt_type = Ndn.INTEREST
        # elif (Ndn.DATA & t) == Ndn.DATA: 
        #     pkt_type = Ndn.DATA

        frag = int(raw[2:4],16)
        f_count = frag & 0xF0
        f_count >>= 4 
        f_index = frag & 0x0F

        chksum = int(raw[4:8],16)
        n_len = 2+int(raw[8:10],16)*2
        p_len = 2+int(raw[10:12],16)*2

        name = binascii.unhexlify( raw[ 12:(12+n_len) ])
        payload = binascii.unhexlify( raw[(12+n_len):])
        
        #print("-FragInfo=>",pkt_type,frag_count,frag_index,len(l),l,payload_len,bin(payload_len))
        return pkt_type, f_count, f_index, p_len, n_len, chksum, name, payload
    
    def chksum(self,data):
        x = 0xFF
        y = 0xFF
        chksum = binascii.hexlify( chr(x)+chr(y) )
        return chksum

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
        #no fragmentation & reassembly 
        chksum = self.chksum(payload)
        f_count = 1 #Single Fragment
        f_index = 0 #Index of the Fragment 
        f_count = f_count << 4 
        opt = f_count | f_index 
        p_len = len(payload)
        n_len = len(name)
        
        encoded = binascii.hexlify(chr(_type))+\
                binascii.hexlify(chr(opt))+\
                chksum+\
                binascii.hexlify(chr(p_len))+\
                binascii.hexlify(chr(n_len))+\
                binascii.hexlify( name )+\
                binascii.hexlify( payload )

        return encoded