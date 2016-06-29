###################### AUTHOR ####################################################
Name: Akshay Satyendra Navale
Occupation: ITP Student at University of Colorado, Boulder.USA.
Contact Details: akna8887@colorado.edu
Phone Number: 720-345-4053
##################################################################################

Welcome!!! 
This is a README file for Stop and wait programs named StopNWaitS.py and StopNWaitR.py.
The python code is written in python version 2.7.

###############StopNWaitS.py file##################################################

This file is a Sender file which takes 3 arguments in following fashion.
1)Filename with extension
2)Ip address of destination
3)Port number of destination

to run this file fire the command as below,
StopNWaitS.py [filename with extention] [IP address of destination]:[Port Number of Destination]
e.g.:
StopNWaitS.py filename.jpg 127.0.0.1:4564

This program check for 
1) validity of the IP address
2) Validity of Port Number (Port number must be greter than 1024 and less than 65535)
3) Presence of file on the in folder
4) Also this code check for file`s size and if it is 0 then it will exit the program with following message.
"File to be send is empty"

###############StopNWaitR.py file######################################################
This program takes only one argument whihch is a port number
This program can be executed as follows:
StopNWaitR.py [Portnumber]

This program check for the port number, you must enter any number between 1024 to 65535

This program saves received file with new name in the same folder. and the new name will 
be always Recevied-[filename].
So if you send a file with name xerox.pdf the receiver will save it as Recevied-xerox.pdf.

###################Setting Packet or Ack loss in Programs################################
In this both programs their is a variable named loss.
For StopNWaitS.py loss variable indicates percentage loss in packets 
On the other hand StopNWaitR.py loss variable indicates percentage loss in acknowledgements.

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

##########################################################################################
Thank You. For your precious time!!!  

 