# -*- coding: utf-8 -*-
import socket
import time
import cv2
import pickle
import numpy as np
import struct ## new
import hashlib

HOST='127.0.0.1'
PORT=8089
delimiter = "|:|:|";
b_delimiter = b'|:|:|'

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind((HOST,PORT))
print ('Socket now listening')
s.connect(('127.0.0.1',8090))


### new
sdata = b""
data = b''
payload_size = struct.calcsize("L") 
#time1 = time.time()

while True:
    i = 0
    seqNoFlag = 0
    length = b""
    data = b""
    sdata = b""
    while len(length) < payload_size:
        length,addr = s.recvfrom(65535)
  #  print(len(length))
    msg_size = struct.unpack("L", length)[0]
    
    while len(sdata) < msg_size:
        data,addr = s.recvfrom(61501)
    #    print(len(data))
        if i == 1:
            ta = time.time()
        i += 1
      #  print (i)              
        new_data = data.split(b_delimiter)[3]
        data = data.split(b_delimiter)[0] + b_delimiter + data.split(b_delimiter)[1] + b_delimiter + data.split(b_delimiter)[2]
        data = data.decode()
        seqNo = data.split(delimiter)[1]
        clientHash = hashlib.sha1(new_data).hexdigest()
        if data.split(delimiter)[0] == clientHash and seqNoFlag == int(seqNo == True):
            packetLength = data.split(delimiter)[2]
            sdata += new_data
            s.sendto((str(seqNo)+ "," + packetLength).encode(),('127.0.0.1',8090))
        else:
   #         print ("Checksum mismatch detected, dropping packet")
            continue;
        if int(packetLength) < 61501:
            seqNo = int(not seqNo)
            
    frame_data = sdata[:msg_size]     
    frame=pickle.loads(frame_data)
    cv2.imshow('frame',frame)
    cv2.waitKey(1)
    
time2 = time.time()
