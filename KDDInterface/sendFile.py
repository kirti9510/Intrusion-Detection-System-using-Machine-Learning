from socket import socket, AF_INET, SOCK_DGRAM
import sys

s = socket(AF_INET,SOCK_DGRAM)
host = 'localhost'
port = 5000

addr = (host,port)

file_name = sys.argv[1]

f=open(file_name,"r")
lines = f.readlines()

for data in lines:
    if(s.sendto(data,addr)):
        print "sending ..."

s.close()
f.close()
