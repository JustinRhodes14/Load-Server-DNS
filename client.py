import threading
import time
import random
import sys
import socket

def sendQueries(queries,sock):
    file = open("RESOLVED.txt","w")
    qLength = len(queries)

    sock.send(str(qLength).encode('utf-8'))
    sock.recv(100)

    for item in queries:
        msg = str(len(item))
        sock.send(msg.encode('utf-8'))
        sock.recv(100)
        sock.send(item.encode('utf-8'))
        sock.recv(100)
        sock.send("ready")

        #Receive message back from LS after it queries from ts1 & ts2

if len(sys.argv) < 3:
    print(
        "Invalid arguments, please use the following to start the client: python client.py <lsHostname> <lsListenPort>")
    exit()

lsHost = sys.argv[1]
lsPort = int(sys.argv[2])

#Read in hostnames to be queried
file = open("PROJ2-HNS.txt", "r")
toQuery = file.read().splitlines()
#print(toQuery)
file.close()

# Establish client/server connection
try:
    cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[C]: Client socket created")
except socket.error as err:
    print('socket open error: {} \n'.format(err))
    exit()

# Define the port on which you want to connect to the server
localhost_addr = socket.gethostbyname(socket.gethostname())

# connect to the server on local machine
server_binding = (lsHost, lsPort)
cs.connect(server_binding)

# Receive data from the server
data_from_server = cs.recv(100)
print("[C]: Data received from server: {}".format(data_from_server.decode('utf-8')))

#Send queries below stored inside toQuery

sendQueries(toQuery,cs)