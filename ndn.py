TLV_INTEREST = ord('\x01')
TLV_DATA = ord('\x02')

def parse_tcilv(t,ci,l):

    '''
        | t = 8-bit Types 
        | c = 4-bit Fragment Count 
        | i = 4-bit Fragment Index
        | l = 16-bit Length     
    '''
    tt = 0
    cc = 0 
    ii = 0
    ll = 0

    if (TLV_INTEREST & t) == TLV_INTEREST:
        tt = TLV_INTEREST
    elif (TLV_DATA & t) == TLV_DATA:
        tt = TLV_DATA

    
    print(tt,TLV_INTEREST,ci,l)

    return tt, cc, ii, ll

class Ndn:
    def __init__(self):
        print("ndn init")
