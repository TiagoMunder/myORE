import base64
import json
from socket import *
import OREDBS
import struct
import crypto


def binarysearchl(cursor,key):
    inf=0;
    sup=len(cursor)-1
    while (inf <= sup):
        mid1 = inf + (sup - inf) / 2
        mid = int(mid1)
        r1 = json.loads(cursor[mid][2])
        nonce = base64.b64decode(cursor[mid][3])
        r1.insert(0, nonce)

        if compare(key,r1) == 0:

            return cursor[mid][4]
        elif compare(key,r1) == -1:
            if inf == sup:
                return cursor[mid][4]
            if inf==mid:
                return cursor[mid][4]

            sup=mid-1
        else:
            if inf == sup:
                return cursor[mid][4]+1

            inf=mid+1
    return -1


def binarysearchR(cursor,key):
    inf=0;
    sup=len(cursor)-1
    while (inf <= sup):
        mid1 = inf + (sup - inf) / 2
        mid = int(mid1)
        r1 = json.loads(cursor[mid][2])
        nonce = base64.b64decode(cursor[mid][3])
        r1.insert(0, nonce)
        if compare(key,r1) == 0:
            return cursor[mid][4]
        elif compare(key,r1) == -1:
            if inf == sup:
                return cursor[mid][4]-1
            if inf==mid:
                return cursor[mid][4] -1
            sup=mid-1
        else:
            if inf == sup:
                return cursor[mid][4]
            inf=mid+1
    return -1

def binarysearch(cursor,key):
    inf=0;
    sup=len(cursor)-1
    global flagequal
    while (inf <= sup):
        mid1 = inf + (sup - inf) / 2
        mid = int(mid1)
        r1 = json.loads(cursor[mid][2])
        nonce = base64.b64decode(cursor[mid][3])
        r1.insert(0, nonce)

        if compare(key,r1) == 0:
            flagequal=1
            return cursor[mid][4]
        elif compare(key,r1) == -1:
            if inf == sup:
                return cursor[mid][4]
            if inf==mid:
                return cursor[mid][4]

            sup=mid-1
        else:
            if inf == sup:

                if (len(cursor) >= mid + 2):
                    r1 = json.loads(cursor[mid][2])
                    nonce = base64.b64decode(cursor[mid][3])
                    r1.insert(0, nonce)
                    if (compare(key, r1) == 0):
                        flagequal = 1
                        return cursor[mid + 1][4]
                return cursor[mid][4]+1

            inf=mid+1
    return -1
def compare(ctl, ctr):
    ctl_r,ctl_l  = ctl
    r = ctr[0]

    result = ( ctr[ctl_r + 1]- (int.from_bytes(crypto.prf_hmac(ctl_l, r), 'big'))) % 3

    if result == 2:
        return -1
    else:
        return result

def send_msg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    #print(len(msg))
    sock.sendall(msg)


def is_empty(any):
    if any:
        return False
    else:
        return True

index=-1
flagequal=0# flag to insert an age that already exists

#OREDBS.TABLE()
#OREDBS.MASTERTABLE()

HOST = "192.168.223.2" #local host
PORT = 6667 #open port 7000 for connection
s = socket(AF_INET, SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1) #how many connections can it receive at one time

while True:
    conn, addr = s.accept()  # accept the connection
    print("Connected by: ", addr)  # print the address of the person connected
    option = conn.recv(1024).decode("UTF-8")  # CTR lista em formato string
    conn.send(bytes("Message" + "\r\n", 'UTF-8'))
    print("sended!")
    if option=="Inserir":
        data = conn.recv(1024).decode("UTF-8") #CTR lista em formato string
        print ("Received: ", data)
        datalista = json.loads(data)# CTR lista em formato Lista
        conn.send(bytes("Message" + "\r\n", 'UTF-8'))
        print("sended!")
        data4 = conn.recv(1024).decode("UTF-8")  # nonce em string encoded em b64
        print("Received: ", data4)
        Noncedecoded = base64.b64decode(data4)  # nonce em bytes
        datalista.insert(0, Noncedecoded)       # Inserir Nonce na primeira posição da lista
        conn.send(bytes("Message" + "\r\n", 'UTF-8'))
        print("sended!")
        data2 = conn.recv(1024).decode("UTF-8")  # how many bytes of data will the server receive
        print("Received: ", data2)
        age=int(data2)                           #Passar idade de String para inteiro
        conn.send(bytes("Message" + "\r\n", 'UTF-8'))
        print("sended!")
        data3 = conn.recv(1024).decode("UTF-8")  # how many bytes of data will the server receive
        print("Received: ", data3)
        encodeddata = base64.b64decode(data3)    #key_l em bytes
        l1 = age, encodeddata
        OREDBS.InsertMaster(age)
        id_m = OREDBS.getIDByPOS(age)
        int1 = id_m[len(id_m) - 1][0]
        res = OREDBS.CTRORDER()

        if is_empty(res):
            OREDBS.Insert(data, data4, 0, int1)
        else:
            index = binarysearch(res, l1)

            if index == -1:
                OREDBS.Insert(data, data4, res[len(res) - 1][4] + 1, int1)
            elif flagequal == 1:
                OREDBS.Insert(data, data4, index, int1)
            else:
                resnew = OREDBS.CTRORDERMORE(index)
                for x in range(0, len(resnew)):
                    OREDBS.Update(resnew[x][0], resnew[x][4] + 1)
                OREDBS.Insert(data, data4, index, int1)
        conn.send(bytes("Message" + "\r\n", 'UTF-8'))
        print("sended!")
        print(flagequal)
        flagequal = 0
        index = -1



    if option=="range":

        #range query
        data2 = conn.recv(1024).decode("UTF-8")  # how many bytes of data will the server receive
        print("Received: ", data2)
        age = int(data2)
        conn.send(bytes("Message" + "\r\n", 'UTF-8'))
        print("sended!")
        data3 = conn.recv(1024).decode("UTF-8")  # how many bytes of data will the server receive
        print("Received: ", data3)
        encodeddata = base64.b64decode(data3)  # key_l in bytes
        conn.send(bytes("Message" + "\r\n", 'UTF-8'))
        print("sended!")
        data5 = conn.recv(1024).decode("UTF-8")  # how many bytes of data will the server receive
        print("Received: ", data5)
        age2 = int(data5)
        conn.send(bytes("Message" + "\r\n", 'UTF-8'))
        print("sended!")
        data6 = conn.recv(1024).decode("UTF-8")  # how many bytes of data will the server receive
        print("Received: ", data6)
        encodeddata2 = base64.b64decode(data6)  # key_l in bytes
        l1=age,encodeddata
        l2=age2,encodeddata2
        res = OREDBS.CTRORDER()
        lowerindex = binarysearchl(res, l1)
        print("lower=", lowerindex)
        if lowerindex == -1:
            lowerindex = res[len(res) - 1][4] + 1

        maxindex = binarysearchR(res, l2)
        print("max=", maxindex)
        if maxindex == -1:
            maxindex = res[0][4]

        res3 = OREDBS.getRangeID(lowerindex, maxindex)
        result=[]
        for j in range(0, len(res3)):
            print(res3[j][0])
            result.append(res3[j][0])
        result = json.dumps(result)
        conn.send(bytes(result + "\r\n", 'UTF-8'))
        print("sended!")
    if option=="exit":
        break;




    conn.close()




