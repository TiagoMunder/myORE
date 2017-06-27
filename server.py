import struct

import OREDBS
from ore import OreScheme
import crypto
import json
import socket
import base64
import zlib
import time


def send_msg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    #print(len(msg))
    sock.sendall(msg)

def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    #print(msglen)
    # Read the message data
    return recvall(sock, msglen)

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = b""
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data



def is_empty(any):
    if any:
        return False
    else:
        return True



def compare(ctl, ctr):
    ctl_r,ctl_l  = ctl
    r = ctr[0]

    result = (ctr[ctl_r + 1] - (int.from_bytes(crypto.prf_hmac(ctl_l, r), 'big'))) % 3

    if result == 2:
        return -1
    else:
        return result


def binarysearch(cursor,key):
    inf=0;
    sup=len(cursor)-1
    mid=-1
    while (inf <= sup):
        encodeddata = cursor[mid][2].encode()
        encodeddata = base64.b64decode(encodeddata)
        r1decompressed = zlib.decompress(encodeddata)
        r1string = r1decompressed.decode()
        r1 = json.loads(r1string)
        nonce = base64.b64decode(cursor[mid][3])
        r1.insert(0, nonce)
        mid=(inf+sup)/2
        if compare(key,r1) == 0:
            return mid
        elif compare(key,r1) == -1:
            sup=mid-1
        else:
            if inf==mid:
                return mid

            inf=mid-1
    return -1


bd=OREDBS.connection()
print(bd)

#OREDBS.TABLE()
#OREDBS.MASTERTABLE()










TCP_IP = "127.0.0.1"
TCP_PORT = 6667
BUFFER_SIZE = 1024

mok="ok"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
conn, addr = s.accept()
#print ('Connection address:', addr)
index=-1


while 1:
    data2 = conn.recv(BUFFER_SIZE).decode()
    #data2 = recv_msg(conn).decode()  # receive vector
    #print ("server recieved ",data2)




    conn.send(mok.encode())
    if data2 == 'inserir':
        counter=0
        #data3 = conn.recv(BUFFER_SIZE).decode()#receive vector
        data3=recv_msg(conn).decode()
        data3comp=zlib.compress(data3.encode("ascii"))
        conn.send(mok.encode())
        #data4 = conn.recv(BUFFER_SIZE).decode('latin-1')#receive nonce and decode from bytes to string
        #data4 = conn.recv(BUFFER_SIZE)# receive nonce in bytes b64
        data4 = recv_msg(conn)
        noncestring = data4.decode()# nonce bytes to string
        conn.send(mok.encode())  # echo
        #cry = conn.recv(BUFFER_SIZE)
        cry=recv_msg(conn)
        conn.send(mok.encode())
        #pos = conn.recv(BUFFER_SIZE)
        pos=recv_msg(conn)
        pos2 = int.from_bytes(pos, 'big')
        #print(pos2)
        l1 = pos2, cry
        OREDBS.InsertMaster(pos2)
        data3comp = base64.b64encode(data3comp)  # bytes to bytes in mode 64
        data3compde=data3comp.decode()
        id_m=OREDBS.getIDByPOS(pos2)
        int1=id_m[len(id_m)-1][0]
        res=OREDBS.CTRORDER()
        flagequal=0# flag to insert an age that already exists
        start_time = time.clock()
        if is_empty(res):
            OREDBS.Insert(data3compde, noncestring, 0, int1)
        else:
            for i in range(0, len(res)):
                encodeddata = res[i][2].encode()
                encodeddata = base64.b64decode(encodeddata)
                r1decompressed = zlib.decompress(encodeddata)
                r1string=r1decompressed.decode()
                r1 = json.loads(r1string)
                nonce = base64.b64decode(res[i][3])
                r1.insert(0, nonce)
                #print( "boas",compare(l1, r1))
                if compare(l1, r1) == -1:
                    index = res[i][4]
                    break
                elif compare(l1, r1) == 0:
                    flagequal=1
                    index = res[i][4]
                    break
                else:
                    if i==0:
                        counter=counter+1
                    elif res[i-1][4]!=res[i][4]:
                        counter = counter + 1
                    else:
                        continue

            if index == -1:
                OREDBS.Insert(data3compde, noncestring, counter, int1)
            elif flagequal==1:
                OREDBS.Insert(data3compde, noncestring, index, int1)
            else:
                resnew = OREDBS.CTRORDERMORE(index)
                for x in range(0, len(resnew)):
                    OREDBS.Update(resnew[x][0], resnew[x][4] + 1)
                OREDBS.Insert(data3compde, noncestring, index, int1)
        conn.send(mok.encode())  # echo
        flagequal=0
        index=-1
        print(time.clock() - start_time, "seconds")
        continue
    if data2 == "delete":
        cry = conn.recv(BUFFER_SIZE)# secret key
        conn.send(mok.encode())
        pos = conn.recv(BUFFER_SIZE) #pos in bytes
        pos2 = int.from_bytes(pos, 'big')#bytes to int
        conn.send(mok.encode())
        l1 = pos2, cry
        res = OREDBS.CTRORDER()
        if is_empty(res):
            print("Database is empty")
        else:
            index=-1
            for i in range(0, len(res)):
                encodeddata = res[i][2].encode()
                encodeddata = base64.b64decode(encodeddata)
                r1decompressed = zlib.decompress(encodeddata)
                r1string = r1decompressed.decode()
                r1 = json.loads(r1string)
                nonce = base64.b64decode(res[i][3])
                r1.insert(0, nonce)
                print("boas", compare(l1, r1))
                if compare(l1, r1) == 0:
                    index = res[i][4]
                    OREDBS.deleteX(res[i][1])

            if index!=-1:
                resnew = OREDBS.CTRORDERMORE(index+1)
                if is_empty(resnew):
                    print("No More indices to Update")
                else:
                    for x in range(0, len(resnew)):
                        OREDBS.Update(resnew[x][0], resnew[x][4] - 1)

        print(time.clock() - start_time, "seconds")
        continue
    if data2 == 'getInt':
        cry = conn.recv(BUFFER_SIZE)
        conn.send(mok.encode())
        pos=conn.recv(BUFFER_SIZE)
        pos2=int.from_bytes(pos,'big')
        l1=pos2,cry
        conn.send(mok.encode())  # echo
        res=OREDBS.CTR()
        for i in range(0,len(res)):
            encodeddata = res[i][2].encode()
            encodeddata = base64.b64decode(encodeddata)
            r1decompressed = zlib.decompress(encodeddata)
            r1string = r1decompressed.decode()
            r1 = json.loads(r1string)
            nonce=res[i][3].encode('latin-1')
            r1.insert(0,nonce)
            print(compare(l1,r1))

        continue
    if data2 == 'getrange':
        lowerindex=0;
        maxindex=0;
        cry = conn.recv(BUFFER_SIZE)
        conn.send(mok.encode())
        cry2 = conn.recv(BUFFER_SIZE)
        conn.send(mok.encode())
        pos = conn.recv(BUFFER_SIZE)
        pos = int.from_bytes(pos, 'big')
        conn.send(mok.encode())
        pos2 = conn.recv(BUFFER_SIZE)
        pos2 = int.from_bytes(pos2, 'big')
        l1 = pos,cry
        l2 = pos2,cry2
        conn.send(mok.encode())  # echo
        start_time = time.clock()
        res = OREDBS.CTRORDER()
        for i in range(0, len(res)): #cycle for to find lower index
            encodeddata = res[i][2].encode()
            encodeddata = base64.b64decode(encodeddata)
            r1decompressed = zlib.decompress(encodeddata)
            r1string = r1decompressed.decode()
            r1 = json.loads(r1string)
            nonce = base64.b64decode(res[i][3])
            r1.insert(0, nonce)
            if compare(l1, r1) == 1:
                continue
            elif compare(l1, r1) == -1:
                lowerindex = res[i][4]
                break
            else:
                lowerindex = res[i][4]
                break
        for i in range(0, len(res)): #cycle for to find upper index
            encodeddata = res[i][2].encode()
            encodeddata = base64.b64decode(encodeddata)
            r1decompressed = zlib.decompress(encodeddata)
            r1string = r1decompressed.decode()
            r1 = json.loads(r1string)
            nonce = base64.b64decode(res[i][3])
            r1.insert(0, nonce)
            if compare(l2,r1) == 1:
                maxindex=res[i][4]

            elif compare(l2,r1) == -1:
                break

            else:
                maxindex = res[i][4]
                break

        res3 = OREDBS.getRangeID(lowerindex,maxindex)
        print(time.clock() - start_time, "seconds")
        for j in range(0,len(res3)):
            print(res3[j][0])





    if data2 == "exit":
        break


