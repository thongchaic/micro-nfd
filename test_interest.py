import socket
import sys
import os
import time 
import ndn

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('192.168.6.153', 6363)

def test_send():
        c = 1
        try:
                #send_at = int(round(time.time() * 1000))
                while c < 5:
                        name = "/ndn/th/ac/srru/good2cu*99/"+str(c)
                        name_len = len(name)
                        pkt_len = ''

                        x = name_len&0x00FF
                        y = name_len&0xFF00
                        y >>= 8
                        print(y,x,bin(y),bin(x),bin(name_len))
                        interest = chr(ndn.TLV_INTEREST)+chr(int('00010001', 2))+chr(y)+chr(x)+pkt_len+name
                        print(interest)
                        sock.sendto(interest, server_address)
                        #now = int(round(time.time() * 1000))
                        #if (now - send_at) > (1000*60):
                        #        print( str(c),' packets sended...')
                        #        break
                        time.sleep(0.1)
                        c = c + 1
        finally:
                print('----end----')

if __name__ == '__main__':
        test_send()
