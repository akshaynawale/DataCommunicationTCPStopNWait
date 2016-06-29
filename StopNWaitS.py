import sys, socket, re, os, time
import random

Packsize=1024
Timeout=0.5
Loss=0

def GetArguments(): # this function checks the arguments and return them to main code
    if (len(sys.argv)!=3):
        print("This program requires 2 arguments Filename, Destination IP:Destination Port")
        sys.exit()
    Filename=sys.argv[1]
    IpPort= sys.argv[2]
    IpPort=IpPort.split(":")
    IP=IpPort[0]
    Port=IpPort[1]
    try:
        Port=int(Port)
    except:
        print("The Port must be a integer")
        sys.exit()
    if ((Port <1025) or (Port>65535)): 
        print("The port number must be between 1025 to 65535")
        sys.exit()
    IPWrong=False
    IPSplit=IP.split(".")
    for Num in IPSplit:
        try:
            Num=int(Num)
        except:
            print("The IP address you have entered is wrong")
            sys.exit()
        if (Num > 255) :
            IPWrong=True
    if IPWrong:
        print("IP you have entered is wrong")
        sys.exit()
        
    if not (os.path.isfile(Filename)):
        print("File Does not exists")
        sys.exit()
        
    return IP, Port, Filename 

def CalculatePacketsFilesize(Filename, Packsize):   # calculates packet size and total number of data packets
    Filesize=os.path.getsize(Filename)
    Filesize=int(Filesize)
    TotalPackets=(Filesize/Packsize)
    
    roundedpac=round(TotalPackets)
    if (roundedpac < TotalPackets):
        TotalPackets=roundedpac+1
    else:
        TotalPackets=roundedpac
    return Filesize, TotalPackets


def SendInitialPacket(Filename, SeqNumber, Sock, IP, Port, PacketNumber):   # sends Inital syncronyzation packet
    PacketData=str(SeqNumber)+"|||syn|||"+str(Filename)
    DestAddress=(IP, Port)
    Sock.sendto(PacketData, DestAddress)
    try:
        Sock.settimeout(Timeout)
        while True:
            data, address= Sock.recvfrom(Port)
            text= data.decode()
            if text:
                textsplit=text.split("|||")
                AckFor=textsplit[0]
                AckFor=int(AckFor)
                #print("\n \n Acknowledgement number:"+str(AckFor))
                if (AckFor == 0):
                    print("Received Syn Acknowledgement")
                    PacketNumber=0
                    return PacketNumber
                else:
                    print("Received Wrong Syn Acknowledgement")
                    return PacketNumber
    except:
        print("timeout for syn packet number : "+str(PacketNumber)+" has happen")
        return PacketNumber

def SendPacket(Filename, IP, Port, Sock, Pointer, Packsize, SeqNumber, PacketNumber):   # Sends data packet
    hand=open(Filename,'rb')
    hand.seek(Pointer)
    senddata=hand.read(Packsize)
    PacketData=str(SeqNumber)+"|||data|||"+str(senddata)
    server_address = (IP, Port)
    print("Sending Packet : "+str(PacketNumber))
    #print("Packet Data : "+PacketData)
    i=random.randint(0,100)
    if(i>Loss) or (Loss==0):        
        Sock.sendto(PacketData, server_address)
    try:
        Sock.settimeout(Timeout)
        while True:
            data, address= Sock.recvfrom(Port)
            text=data.decode()
            if text:
                textsplit=text.split("|||")
                AckFor=textsplit[0]
                AckFor=int(AckFor)
                if (SeqNumber == AckFor):
                    print("Acknowledgement for the packet : "+str(PacketNumber)+" received")
                    PacketNumber=PacketNumber+1
                    Pointer=Pointer+Packsize
                    if SeqNumber == 0:
                        SeqNumber = 1
                    else:
                        SeqNumber = 0
                else:
                    print("Packet Loss for Packet "+str(PacketNumber)+" happen")
                return PacketNumber, Pointer, SeqNumber
    except:
        print("timeout for Packet Number :"+str(PacketNumber)+" has happen re-sending the packet")
        return PacketNumber, Pointer, SeqNumber
    

def SendFinalPacket(Sock, IP, Port, SeqNumber, Filename, Final):    # Sends Final Packet
    PacketData=str(SeqNumber)+"|||fin|||" 
    PacketData=PacketData.encode()       
    server_address = (IP, Port)
    print("Final Packet Send: "+str(PacketData))
    Sock.sendto(PacketData, server_address)
    print(str(Filename)+" is successfully send to "+IP+str(Port))
    while True:
        data, address= Sock.recvfrom(Port)
        text= data.decode()
        if text:
            textsplit=text.split("|||")
            AckFor=textsplit[0]
            AckFor=int(AckFor)
            #print("received Ack : "+str(AckFor))
            #print("Required Seq : "+str(SeqNumber))
            if (AckFor == SeqNumber):
                print("Received Acknowledgement for Final packet")
                Final=1
                return Final
            else:
                print("Received Wrong Sequence number for  Final packet")
                return Final

IP, Port, Filename = GetArguments() # Getting inline arguments

Filesize, TotalPackets = CalculatePacketsFilesize(Filename, Packsize)
#print(str(Filesize)+" "+str(TotalPackets))
if Filesize == 0:
    print("File to be send is empty")
    sys.exit()
Sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

PacketNumber=-1
SeqNumber=0
Pointer=0
TotalPackets=int(TotalPackets)
Zal=False
while(PacketNumber!=0):
    #time.sleep(1)
    PacketNumber=SendInitialPacket(Filename, SeqNumber, Sock, IP, Port, PacketNumber)
        
print("Now sending Data Packets")

SeqNumber=1
while(PacketNumber < (TotalPackets+1)):
    #time.sleep(1)
    PacketNumber, Pointer, SeqNumber = SendPacket(Filename, IP, Port, Sock, Pointer, Packsize, SeqNumber, PacketNumber)

Final=0
while(Final == 0):
    Final=SendFinalPacket(Sock, IP, Port, SeqNumber, Filename, Final)
print("Sended Data Successfully with size : "+str(Filesize))
print("Total Packets : "+str(TotalPackets))
sys.exit()