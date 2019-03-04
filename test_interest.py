import socket
import sys
import os
import time 
import ndn

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('192.168.1.17', 6363)

def test_send():
        c = 1
        try:
                #send_at = int(round(time.time() * 1000))
                while c < 5:
                        name = "/ndn/th/ac/srru/"+str(c)
                        l = len(name)
                        interest = chr(ndn.TLV_INTEREST)+str(l)+name
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
