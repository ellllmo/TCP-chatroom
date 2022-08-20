from asyncio.windows_events import NULL
import socket

def receive():
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    #name felan , I look for felan 
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    clientMsg = "Message from Client:{}".format(message)
    clientIP  = "Client IP Address:{}".format(address)
    print(clientMsg)
    print(clientIP)
    message =str(bytesAddressPair[0].decode('utf-8'))
    #print(message[0])
    return message,address



localIP     = "127.0.0.1"
localPort   = 5000

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening ..")

# Listen for incoming datagrams
bufferSize  = 1024
list=[]

while(True):
    return_ris=receive()
    q=0
    #print(address)
    message=return_ris[0].split(" ")
    address=return_ris[1]
    if message[0]=="name" and message[1]!=NULL:
        message[2]=message[2]+" "+message[3]
        for w in range(0,len(list),3):
            if list[w]==message[1]:
                q=-1
                msgFromServer = "this name are reserved enter another one!"
                bytesToSend = str.encode(msgFromServer)
                UDPServerSocket.sendto(bytesToSend, address)
                break
        if q==0:
            list.append(message[1])
            list.append(address)
            list.append(message[2])
            msgFromServer = "Hello "+message[1]
            bytesToSend = str.encode(msgFromServer)
            UDPServerSocket.sendto(bytesToSend, address)
        q=0
    elif message[1]=="exit":
        msgFromServer = "goodbye"
        bytesToSend = str.encode(msgFromServer)
        UDPServerSocket.sendto(bytesToSend, address)
    elif message[0]=="search" and message[1]!=NULL:
        for w in range(0,len(list)-2,3):
            if list[w]==message[1]:
                q=-1
                msgFromServer = message[1]+" :"+(list[w+2])
                bytesToSend = str.encode(msgFromServer)
                UDPServerSocket.sendto(bytesToSend, address)
                break
        if q==0:
            msgFromServer = message[1]+" is not in list!"
            bytesToSend = str.encode(msgFromServer)
            UDPServerSocket.sendto(bytesToSend, address)
        q=0

   