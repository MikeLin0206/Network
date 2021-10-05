# -*- coding: utf-8 -*-
import cv2
import numpy as np
import socket
import time
import pickle
import struct
import datetime
import hashlib

HOST='127.0.0.1'
PORT=8089
address = (HOST,PORT)
delimiter = "|:|:|"
seqFlag = 0
ta = 0

class packet():
    checksum = 0;
    length = 0;
    seqNo = 0;
    msg = 0;

    def make(self, data):
        self.msg = data
        self.length = str(len(data))
        self.checksum=hashlib.sha1(data).hexdigest()

cap=cv2.VideoCapture("test3.mp4")
clientsocket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
clientsocket.bind(('127.0.0.1',8090))
#clientsocket.connect(('localhost',8089))

cframe = 0
time1 = time.time()
while True:
    # Serialize frame
    rat,frame = cap.read()
    if not rat:
        break
    data = pickle.dumps(frame)
    message_size = struct.pack("L", len(data))
    x = 0
    start_time=time.time()
    resend = 0;
    pkt = packet()
    sent = clientsocket.sendto(message_size,address)
    
    for i in range(46):
        msg = data[i*61440:(i+1)*61440]
        pkt.make(msg);
        finalPacket = str(pkt.checksum) + delimiter + str(pkt.seqNo) + delimiter + str(pkt.length) + delimiter# + str(pkt.msg)
        finalPacket = finalPacket.encode() + pkt.msg
        clientsocket.sendto(finalPacket,address)
       # print('Sent {} bytes back to {}, awaiting acknowledgment..'.format(sent, "('127.0.0.1',50008)"))
        clientsocket.settimeout(0.1)
        try:          
            ack,address = clientsocket.recvfrom(100)
            ack = ack.decode()
         #   print("got ack")
                    #break
        except:
         #   print ("Time out reached, resending ...",x);
            resend += 1;
         #   print("Resend:",resend)
            continue;
        if ack.split(",")[0] == str(pkt.seqNo):
            pkt.seqNo = int(not pkt.seqNo)
          #  print ("Acknowledged by: " + ack + "\nAcknowledged at: " + str(
          #          datetime.datetime.utcnow()) + "\nElapsed: " + str(time.time() - start_time))
            x += 1
          #  print("x = ",x)
            
    cframe += 1
    if cframe == 36:
        time2 = time.time()
        print("{:.4f}".format(time2 - time1))
    if cframe == 181:
        time2 = time.time()
        print("{:.4f}".format(time2 - time1))
    if cframe == 362:
        time2 = time.time()
        print("{:.4f}".format(time2 - time1))

time2 = time.time()

#2764964