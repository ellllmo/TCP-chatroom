import socket
import threading
import time
import sys

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
serverAddressPort= ("127.0.0.1",5000)
bufferSize = 1024
tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
block_list=[]
tcpip="127.0.0.1"
tcpport=0

def convert_to_tuple(peerAddressPort):
    list=peerAddressPort.split(", ")
    peerIP=(list[0][2:-1])
    peerPORT=int(list[1][0:-1])
    peerAddressPort=(peerIP,peerPORT)
    return peerAddressPort

    #for new connection
def start_connection():
    global peer_list,tcpSocket,TCPaddr
    while True:
        try:
            peer2, addr = tcpSocket.accept() 
            msgpeer = peer2.recvfrom(bufferSize)
            msg=msgpeer[0].decode('utf-8')
            msg=msg.split(" : ")
            #print("\n"+str(msg[0])+":"+str(msg[1])+"\n")
            #print(msgpeer[1])
            peeraddress=convert_to_tuple(msg[2])
        except socket.error:
            continue  
        username=msg[0]
        if username not in block_list:
            #this message send to client after you want to connection (Enter 2)
            if msg[1]=="start connection":
                if username not in peer_list:
                    tcppeer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    tcppeer.connect(peeraddress)
                    message=f"{myname} : start connection : {TCPaddr}"
                    tcppeer.send(str.encode(message))
                    peer_list.append(username)
                    peer_list.append(peeraddress)
                    peer_list.append(tcppeer)
                    print(f"\nyou are connecting to {username}.\nEnter 2 to continue or start a conversation")
                #check for new message 
                #if client send "start connection" message 
                tread2 = threading.Thread(target=tcp_receive_msg, args=(username,peeraddress,peer2))
                tread2.start()
        else:
            print("you have request from block_list")

    #check for new message 
def tcp_receive_msg (username,address,tcpclient: socket.socket):
    global peer_list,tcpSocket
    try:
        while True:
            if username not in block_list:
                msg = tcpclient.recv(bufferSize).decode("utf-8")
                msg=msg.split(" : ")
                if username not in block_list:
                    print("\n"+str(msg[0])+":"+str(msg[1]))
                #print(address)
    except socket.error:
        print("you can't receive message most probably your friend disconnected !")
        time.sleep(1)
        del peer_list[peer_list.index(username):peer_list.index(username)+3]
        tcpclient.close()

def first():
    print("""
                                 `!'                          
                                ;UUU;                         
                               ;IIIII;                          
                            ~@@@@~|~@@@@~\n~.:.~.:.~.:.~.:.~.:.~.:.~.:.~.:.~.:.~.:.~.:.<>.:.~.:.~.:.~.:.~.:.~.:.~\n
                              WELLCOME\n
                    Now you have TCP and UDP connection!\n
~.:.~.:.~.:.~.:.~.:.~.:.~.:.~.:.~.:.~.:.~.:.<>.:.~.:.~.:.~.:.~.:.~.:.~
                            ~@@@@~|~@@@@~
                               ;IIIII;                          
                                ;UUU;                         
                                 `!'                         \n""")
    
def menu():
    global myname,peer_list,TCPaddr,block_list
    print("   1.Start new connection \t2.Continue conversation \t3.Block user \t4.Exit")
    w=int(input("Write the number you want : "))
    if w==1:
        message1=input("write the name that you want to find :")
        message="search "+message1
        bytesToSend= str.encode(message)
        UDPClientSocket.sendto(bytesToSend, serverAddressPort)
        msgServer = UDPClientSocket.recvfrom(bufferSize)
        print("SERVER : "+msgServer[0].decode('utf-8'))

        #if the name is not in list ask again
        while msgServer[0].decode('utf-8')==(message1+" is not in list!"):
            time.sleep(1)
            menu()
        
        peer=msgServer[0].decode('utf-8')
        peer=peer.split(":")
        peerAddressPort=peer[1]
        if peer[0] in peer_list:
            print(f"you have connected to {peer[0]} Enter 2 to continue or start a conversation")
            time.sleep(0.7)

        else:
            try:
                tcppeer=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                peerAddressPort=convert_to_tuple(peerAddressPort)
                tcppeer.connect(peerAddressPort)
                message=myname+" : "+"start connection"+" : "+str(TCPaddr)
                bytesToSend= str.encode(message)
                tcppeer.sendto(bytesToSend,peerAddressPort)
                peer_list.append(peer[0])
                peer_list.append(peer[1])
                peer_list.append(tcppeer)
            except socket.error:
                print("you can't connect  most probably your friend disconnected !")
                tcppeer.close()

        menu()

    elif w==2:
        username=input("write the username that you have connection with her/him :")
        if username in peer_list:
            peer2=peer_list[peer_list.index(username)+2]
            msg=myname+" : "+input("write your message :")
            peer2.sendall(msg.encode('utf-8'))
        else:
            print(f"you dont have connection with {username} Enter 1 to  start a connection!")
        time.sleep(0.7)
        menu()

    elif w==3:
        user=input("write the username that you want block : ")
        block_list.append(user)
        if user in peer_list:
                del peer_list[peer_list.index(user):peer_list.index(user)+3]
        print(f"you block {user}")
        print("\n\t\tBlock List:\n")
        print(block_list)
        time.sleep(1)
        menu()
        
    elif w==4:
        message1="exit"
        message="search "+message1
        bytesToSend= str.encode(message)
        UDPClientSocket.sendto(bytesToSend, serverAddressPort)
        msgServer = UDPClientSocket.recvfrom(bufferSize)
        print("SERVER : "+msgServer[0].decode('utf-8'))
        UDPClientSocket.close()
        sys.exit()

    else:
        print("! It's not valid !")
        time.sleep(1)
        menu()

def main():

    global tcpip,tcpport,peer_list,myname,TCPaddr

    #find empty port in our machine for tcp server
    tcpSocket.bind((tcpip,tcpport))
    tcpSocket.listen(5)
    tcpport= tcpSocket.getsockname()[1]
    TCPaddr=(tcpip,tcpport)
    thread = threading.Thread(target=start_connection)
    thread.start()

    #use "name " to get protocol to message
    message="name "+input("write your name :")+" "+str(TCPaddr) #send tcp address with message for client can connect to me
    #convert to byte
    bytesToSend= str.encode(message)
    #send tcp address for client
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    msgServer = UDPClientSocket.recvfrom(bufferSize)
    print("SERVER : "+msgServer[0].decode('utf-8'))

    #if the name is exist do it again and again
    while msgServer[0].decode('utf-8')=="this name are reserved enter another one!":
        message="name "+input("write your name :")+" "+str(TCPaddr) #send tcp address for client can connect to me
        bytesToSend= str.encode(message)
        #send tcp address for client 
        UDPClientSocket.sendto(bytesToSend, serverAddressPort)
        msgServer = UDPClientSocket.recvfrom(bufferSize)
        print("\nSERVER : "+msgServer[0].decode('utf-8'))
    message=message.split(" ")
   
    #save my username
    myname=message[1]
    
    #peer_list is a list of clients that connect to me
    peer_list=[]

    #Pause the code for a few seconds to read what print
    time.sleep(1)
    first()
    menu()

if __name__ == '__main__':
    main()
