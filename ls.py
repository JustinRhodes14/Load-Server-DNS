import threading
import time
import random
import sys
import socket

if len(sys.argv) != 6:
    print("Invalid arguments, please use the following to start the server: python ls.py lsListenPort ts1Hostname ts1ListenPort ts2Hostname ts2ListenPort")
    exit()

portNum = int(sys.argv[1])
ts1Host = sys.argv[2]
ts1Port = int(sys.argv[3])
ts2Host = sys.argv[4]
ts2Port = int(sys.argv[5])
#Establish server socket
try:
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[S]: Server socket created")
except socket.error as err:
    print('socket open error: {}\n'.format(err))
    exit()

server_binding = ('', portNum)
ss.bind(server_binding)
ss.listen(1)
host = socket.gethostname()
print("[S]: Server host name is {}".format(host))
localhost_ip = (socket.gethostbyname(host))
print("[S]: Server IP address is {}".format(localhost_ip))
csockid, addr = ss.accept()
print ("[S]: Got a connection request from a client at {}".format(addr))

# send a intro message to the client.  
msg = "Successfully connected, waiting for queries..."
csockid.send(msg.encode('utf-8'))

#Receive number of queries

qLength = csockid.recv(100)
csockid.send("success")
x = int(qLength)

for i in range(x):
    msg = csockid.recv(100)
    csockid.send("success")
    msgLen = int(msg)
    msg = csockid.recv(msgLen)
    csockid.send("success")
    csockid.recv(100)
    result = ""
    print(msg)

    #Do stuff below connecting to both ts1 and ts2 to query each table


csockid.recv(100) #This is temporary, just so we can insta start the ls each time
csockid.close()