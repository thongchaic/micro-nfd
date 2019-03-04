TLV_INTEREST = ord('\x01')
TLV_DATA = ord('\x02')

def parse_tcilv(t,ci,l):

    t = 0
    c = 0
    i = 0
    l = 0
    if (TLV_INTEREST & t) == TLV_INTEREST:
        t = TLV_INTEREST
    elif (TLV_DATA & t) == TLV_DATA:
        t = TLV_DATA

    
    return t, c, i, l
class Ndn:
    def __init__(self):
        print("ndn init")

