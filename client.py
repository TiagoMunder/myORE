import struct

from ore import OreScheme
import crypto
import OREDB
import json
import socket
import base64
import zlib
from random import randint

def send_msg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    #print("client size", len(msg))
    sock.sendall(msg)
    #print("sent")



def int_to_bytes(x):
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')
message_space = 16
bd=OREDB.connection()
#print(bd)




TCP_IP = '127.0.0.1'
TCP_PORT = 6667
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))



#prf_key = crypto.generate_random(2**message_space)

file = open("prf.txt","r")

prf_key=file.read()
prf_key2=prf_key.encode()
#for k in range (1,1000):
    #randomage=randint(50, 300)
ore1 = OreScheme(200, prf_key2, namespace=2**message_space)
ore2 = OreScheme(250, prf_key2, namespace=2**message_space)
l1, r1 = ore1.encrypt()
l2,r2=ore2.encrypt()
cry,pos=l1
cry2,pos2=l2

#crystring=cry.decode('utf-8') #bytes to string
#crystring2=cry2.decode('utf-8') #bytes to string
#OREDB.Insert(pos, crystring)
#OREDB.Insert(pos2, crystring2)
non = r1[0]#1
r1.pop(0)
teste=r1
non1 = base64.b64encode(non)# bytes to bytes in mode 64
#print("original r1 size ", len(r1) )
r1 = json.dumps(r1)#

non2=r2[0]#2
r2.pop(0)
non2=base64.b64encode(non2)# bytes to bytes in mode 64
r2=json.dumps(r2)#2


"""
message='inserir'
s.send(message.encode())
#mybytes = message.encode()
#send_msg(s,mybytes)

data = s.recv(BUFFER_SIZE).decode()
#s.send(r1.encode())#send vector
r1bytes = r1.encode()
#print("length of r1 ",len(r1),"  and in bytes ", len(r1bytes))
r1compressed = zlib.compress(r1.encode())
#print("length of r1compressed is ",len(r1compressed))
datacomp = base64.b64encode(r1compressed)
decodeddata=datacomp.decode()
#print("length of decoded is ",len(decodeddata))
encodeddata=decodeddata.encode()
encodeddata = base64.b64decode(encodeddata)
r1decompressed = zlib.decompress(encodeddata)

#if r1decompressed==r1bytes:
    #print("nicenice")
#if r1decompressed.decode()==r1:
    #print("teste=ok")

send_msg(s,r1bytes)



data = s.recv(BUFFER_SIZE).decode()
#s.send(non1)#send nonce in bytes b64
send_msg(s,non1)
data = s.recv(BUFFER_SIZE).decode()
#s.send(cry)
send_msg(s, cry)
data = s.recv(BUFFER_SIZE).decode()
#s.send(int_to_bytes(pos))
send_msg(s, int_to_bytes(pos))
data = s.recv(BUFFER_SIZE).decode()

#message='inserir'
#s.send(message.encode())
#data = s.recv(BUFFER_SIZE).decode()
#s.send(r2.encode())#send vector
#data = s.recv(BUFFER_SIZE).decode()
#s.send(non2)#send nonce
#data = s.recv(BUFFER_SIZE).decode()
#s.send(cry2)
#data = s.recv(BUFFER_SIZE).decode()
#s.send(int_to_bytes(pos2))
#data = s.recv(BUFFER_SIZE).decode()
"""

message='getrange'
s.send(message.encode())
data = s.recv(BUFFER_SIZE).decode()
s.send(cry)
data = s.recv(BUFFER_SIZE).decode()
s.send(cry2)
data = s.recv(BUFFER_SIZE).decode()
s.send(int_to_bytes(pos))
data = s.recv(BUFFER_SIZE).decode()
s.send(int_to_bytes(pos2))
data = s.recv(BUFFER_SIZE).decode()


"""
message='delete'
s.send(message.encode())
data = s.recv(BUFFER_SIZE).decode()
s.send(cry)
data = s.recv(BUFFER_SIZE).decode()
s.send(int_to_bytes(pos))
data = s.recv(BUFFER_SIZE).decode()
"""








message3='exit'
s.send(message3.encode())
data = s.recv(BUFFER_SIZE).decode()

s.close()
