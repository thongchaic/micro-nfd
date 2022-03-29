import socket 
import time 

dst = ('192.168.0.101',6363)
buff_size = 512 
sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

encoded = str.encode('0410ffff05062f68656c6c6f776f726c64')
sock.sendto(encoded, dst)
sock.setblocking(False)
n = 10
while n > 0:
    r = sock.recv(1)
    print(r)
    # print(n, encoded," sended!!!")
    # data,addr = sock.recvfrom(buff_size)
    # print(n,data," received => from", addr)
    # n = n-1
    time.sleep(1)