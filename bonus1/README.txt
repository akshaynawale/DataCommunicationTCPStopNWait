###################### AUTHOR ####################################################
Name: Akshay Satyendra Navale
Occupation: ITP Student at University of Colorado, Boulder.USA.
Contact Details: akna8887@colorado.edu
Phone Number: 720-345-4053
##################################################################################

Welcome!!! 
This is a README file for Stop and wait programs named StopNWaitS2.py and StopNWaitR2.py.
The python code is written in python version 2.7.

###############StopNWaitS2.py file##################################################

This file is a Sender file which takes 3 arguments in following fashion.
1)Filename with extension
2)Ip address of destination
3)Port number of destination

to run this file fire the command as below,
StopNWaitS2.py [filename with extention] [IP address of destination]:[Port Number of Destination]
e.g.:
StopNWaitS2.py filename.jpg 127.0.0.1:4564

This program check for 
1) validity of the IP address
2) Validity of Port Number (Port number must be greter than 1024 and less than 65535)
3) Presence of file on the in folder
4) Also this code check for file`s size and if it is 0 then it will exit the program with following message.
"File to be send is empty"

###############StopNWaitR2.py file######################################################
This program takes only one argument whihch is a port number
This program can be executed as follows:
StopNWaitR2.py [Portnumber]

This program check for the port number, you must enter any number between 1024 to 65535

This program saves received file with new name in the same folder. and the new name will 
be always Recevied-[filename].
So if you send a file with name xerox.pdf the receiver will save it as Recevied-xerox.pdf.

###################Setting Packet or Ack loss in Programs################################
In this both programs their is a variable named loss.
For StopNWaitS2.py loss variable indicates percentage loss in packets 
On the other hand StopNWaitR2.py loss variable indicates percentage loss in acknowledgements.

###############Supported File Types######################################################
This Sender and Receiver code is Tested and working fine with following text types:
1. txt file
2. Img File
3. PDF file
4. word document
5. HTML file
6. mp4 file (video)

This programs are written to supports any type of file
 To change the loss setting just change the loss variable value.
 In each code file.
 
##########Default Functioning#############################################################
The timeout for packets is by default set to 500msec
You can change the setting by changing the value of variable "Timeout"


####################Network termination###################################################
A new functionality of network termination is added in this programs:
After Sender receives Ack for its fin packets it goes in wait state for 2 sec.
The receiver sends a Fin packet after it sends Ack for sender fin packet.
When Sender receives Fin packet from receiver with sequence number 0 it respond back with sending Ack to 
Receiver and reset its wait timer.
When receiver receives this Ack from sender it terminates the connection and prints message "Connection closed successfully"
if not then closed connection after sending 6 fin packets that "Connection closed due to unreachable network"
The sender only closes connection when the wait timer expires.

########################### Wait Timer Importance ########################################

If we don`t put wait timer at sender then when the receiver sends fin packets and when it losts and then it again sends fin packet
then this packets will not be addressed by sender. Also their may be a condition that the Ack from the sender is lost and so the 
reciver not get the Ack and do it retransmit the final pack with seq 0 to sender. So sender must wait for 2 sec that is the wait timer.
Wait timer handles the problems when the final packet or ack for final packet is lost.

##########################################################################################
Thank You. For your precious time!!!  

 