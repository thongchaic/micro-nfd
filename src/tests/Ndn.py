class NDN:
    
    
    __DEBUG__ = False
    def __init__(self,debug=True):
        print("ndn init")
        self.__DEBUG__= debug

    def parse(t,ci,l):
    '''
        | parse 32 bits header 
        | t = 8-bit Types 
        | c = 4-bit Fragment Count 
        | i = 4-bit Fragment Index
        | l = 16-bit Length     
        | lat = 16 bit   # to support geo routing 
        | lng = 16 bit   # to support geo routing 
    '''

    pkt_type = 0
    frag_count = 0 
    frag_index = 0
    payload_len = 0

    if (TLV_INTEREST & t) == TLV_INTEREST:
        pkt_type = TLV_INTEREST
    elif (TLV_DATA & t) == TLV_DATA:
        pkt_type = TLV_DATA
    else:
        #unsolicited pkt 
        if __DEBUG__:
            print("unsolicited packet")

    frag_count = ci & 0x0F
    frag_index = ci & 0xF0 
    frag_index >>= 4

    payload_len = l[0]
    payload_len <<= 8
    payload_len = payload_len | l[1]
    
    #print("-FragInfo=>",pkt_type,frag_count,frag_index,len(l),l,payload_len,bin(payload_len))
    
    return pkt_type, frag_count, frag_index, payload_len
    