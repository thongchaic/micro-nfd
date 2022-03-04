import binascii

class Ndn:
    MAX_PKT_LENGTH=255 #defined by the sx127x.py library, so much like MTU/MRU  
    INTEREST = 4
    DATA = 5
    NACK = 6 
    JOIN_INTEREST = 7
    JOIN_DATA = 8
    JOIN_REJECTED = 9 

    def __init__(self):
        print("Init...NDN....")
     
    def decode(self, raw="0410ffff05062f68656c6c6f776f726c64"):
        
        if raw is None or len(raw) <= 14:
            return None, None, None, None, None, None, None, None
     
        try:
            pkt_type = int(raw[0:2],16)
            frag = int(raw[2:4],16)
            f_count = frag & 0xF0
            f_count >>= 4 
            f_index = frag & 0x0F

            chksum = int(raw[4:8],16)
            n_len = int(raw[8:10],16)
            p_len = int(raw[10:12],16)

            name = binascii.unhexlify( raw[ 12:(12+(n_len*2)) ])
            payload = binascii.unhexlify( raw[(12+(n_len*2)):])
            
            name = name.decode() if isinstance(name, (bytes)) else name
            payload = payload.decode() if isinstance(payload, (bytes)) else payload
            
            return pkt_type, f_count, f_index, p_len, n_len, chksum, name, payload
        except:
            return None, None, None, None, None, None, None, None 

    def chksum(self,data):
        #x = 0xFF
        #y = 0xFF
        #chksum = binascii.hexlify( chr(x)+chr(y) )
        # crc = binascii.crc32(data)
        # a = crc & 0x000000FF
        # b = crc & 0x0000FF00
        # b >>= 8 
        # c = crc & 0x00FF0000
        # c >>= 16
        # d = crc & 0xFF000000
        # d >= 24 
        crc = binascii.crc_hqx(data,0)
        return crc[2:] #without 0x.. 

    def encode(self,_type,c,i,name,payload):
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
        f_count = c #Single Fragment
        f_index = i #Index of the Fragment 
        f_count = f_count << 4 
        opt = f_count | f_index 
        p_len = len(payload)
        n_len = len(name)
        
        encoded = binascii.hexlify(chr(_type))+\
                binascii.hexlify(chr(opt))+\
                chksum+\
                binascii.hexlify(chr(n_len))+\
                binascii.hexlify(chr(p_len))+\
                binascii.hexlify( name )+\
                binascii.hexlify( payload )

        if not encoded:
            return None 
        return encoded.decode()