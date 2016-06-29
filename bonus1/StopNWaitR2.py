import socket, sys, os, random
loss=0
IP="127.0.0.1"
timeout=0.5

def CheckArg(): #    Getting arguments
    if (len(sys.argv)!=2):
        print("This program require portNumber as a argument")
        sys.exit()
    Port=sys.argv[1]
    try:
        Port=int(Port)
    except:
        print("The port number must be a integer")
        sys.exit()
    if (Port<1025) or (Port>65535):
        print("Port number must be a number between 1025 to 65535")
        sys.exit()
    return Port

def ParseData(text):    #    separating parts of message
    splitted=text.split("|||")
    SeqNumber=splitted[0]
    Flag=splitted[1]
    Data=splitted[2]
    SeqNumber=int(SeqNumber)
    return SeqNumber, Flag, Data

def SendAck(SeqNumber, Sock, Address):  # sending Ack
    AckData=str(SeqNumber)+"|||ACK"
    print(AckData)
	
    Sock.sendto(AckData, Address)
    

def termination(Sock, Address, Port, num, Success): 
    finalPack="0|||final"
    finalPack=finalPack.encode()
    Sock.sendto(finalPack, Address) # sending Final Packet
    try:
        Sock.settimeout(timeout)
        while True:
            data, address= Sock.recvfrom(Port)
            text=data.decode()
            if text:
                textsplit=text.split("|||")
                AckFor=textsplit[0]
                msg=textsplit[1]
                AckFor=int(AckFor)
                if (AckFor==0) and (msg=="finack"):
                    print("Fin Ack received from Sender")
                    num=6
                    Success=True
                    return num, Success # retuening with num=6 ans success= True means connection closed successfully
                else:
                    print("wrong fin ack is received")
    except:
        num=num+1
        Success=False
        return num, Success # returning with success = flase means connection not closed successfully

Port=CheckArg() # calling function to get arguments
Sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
Sock.bind((IP,Port))
Pointer=0
Packsize=1024
SeqNumber=0
PacketNumber=1
while True:
    Data, Address= Sock.recvfrom(Port)
    if Data:
        SeqNum, Flag, Data = ParseData(Data)
        if (SeqNumber==SeqNum):
            if Flag == "syn":   # check if the packet is synchronizing packet 
                SendAck(SeqNumber, Sock, Address)
                Filename=Data
                Filename="Recevied-"+Filename
                Filehandle=open(Filename,'wb')
                if SeqNumber == 0:
                    SeqNumber=1
                else: 
                    SeqNumber=0
            elif Flag == "data":    # if the packet is normal data packet
                i=random.randint(1,100)
                if (i>loss) or (loss==0):
                    SendAck(SeqNumber, Sock, Address)
                else:
                    print("Not sending ACK with Seq Number: "+str(SeqNumber))
                Filehandle.write(Data)  # storing data to the file
                Pointer=Pointer+Packsize
                Filehandle.seek(Pointer)
                if SeqNumber == 0:
                    SeqNumber=1
                else: 
                    SeqNumber=0
            elif Flag == "fin": # if the packet is final packet
                print("final packet Ack Seq: "+str(SeqNumber))
                SendAck(SeqNumber, Sock, Address)
                if SeqNumber == 0:
                    SeqNumber=1
                else: 
                    SeqNumber=0
                Filehandle.close()
                num=0
                Success=False
                while(num<6):   # sends 6 times Final with sequence 0
                    num, Success=termination(Sock, Address, Port, num, Success)     # sends final packet and wait for Ack and return if the connection closed successfully or not
                
                if(Success==True):
                    print("Connection closed Successfully")
                    Sock.close()
                else:
                    print("Connection Closed due to unreachable network")
                    Sock.close()
                    
                FileSize=os.path.getsize(Filename)
                print("file : "+str(Filename)+" Received with size : "+str(FileSize))
                sys.exit()
        else:               # if the received sequence number does not match with the expected sequence number then 
            print("Packet with wrong Sequence number is received : "+str(SeqNum))
            print("Sequence number must be "+str(SeqNumber))
            if SeqNumber == 0:
                SeqNumber=1
            else: 
                SeqNumber=0
            SendAck(SeqNumber, Sock, Address)
            if SeqNumber == 0:
                SeqNumber=1
            else: 
                SeqNumber=0
            