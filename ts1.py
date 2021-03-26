import threading
import time
import random
import sys
import socket

if len(sys.argv) != 2:
    print("Invalid arguments, should be of form: python ts1.py ts1ListenPort")
    exit()

portNum = int(sys.argv[1])

dns = {}
tsHost = ""
file = open("PROJ2-DNSTS1.txt", "r")
for i in file:
    arr = i.split()
    temp = arr[0]
    arr[0] = arr[0].lower() 
    if arr[2] == 'NS':
        tsHost = arr[0]
    else:
        dns[arr[0]] = temp + ' ' + arr[1] + ' ' + arr[2]

#print(dns)
file.close()


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

while True:
    csockid, addr = ss.accept()
    print ("[S]: Got a connection request from a client at {}".format(addr))
    query = csockid.recv(200)

    if query == 'finish':
        break

    result = ""

    if query.lower() in dns:
        result = dns[query.lower()]
        print(result)
        csockid.send(result)

print("[S]: Connection broken from {}".format(addr))