import threading
from time import sleep
import random
import fcntl, os
import sys
import errno
import socket

def tsRequest(domain,th1,tp1,th2,tp2):
    try:
        sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock1.settimeout(2)
        print("[LS]: Connected with TS1 server...")
    except:
        print("Socket open error: {} \n".format(err))
        exit()


    try:
        sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock2.settimeout(2)
        print("[LS]: Connected with TS2 server...")
    except:
        print("Socket open error: {} \n".format(err))
        exit()

    server_binding1 = (th1,tp1)
    server_binding2 = (th2,tp2)

    sock1.connect(server_binding1)
    sock2.connect(server_binding2)

    sock1.send(domain)
    sock2.send(domain)

    result = "Error:HOST NOT FOUND"
    try:
        msg1 = sock1.recv(500)
    except socket.timeout, e:
        err = e.args[0]
        if err == 'timed out':
            sleep(1)
            print("No data available from TS1")
        else:
            print(e)
            sys.exit(1)
    else:
        result = msg1
        #print(msg1)

    try:
        msg2 = sock2.recv(500)
    except socket.error, e:
        err = e.args[0]
        if err == 'timed out':
            sleep(1)
            print("No data available from TS2")
        else:
            print(e)
            sys.exit(1)
    else:
        result = msg2
        #print(msg2)

    sock1.close()
    sock2.close()
    return result


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
    #print(msg)

    #Do stuff below connecting to both ts1 and ts2 to query each table
    result = tsRequest(msg,ts1Host,ts1Port,ts2Host,ts2Port)
    #print("\n RESULT: {} \n".format(result))
    #print(result)
    csockid.send(result)

csockid.recv(100) #This is temporary, just so we can insta start the ls each time
csockid.close()