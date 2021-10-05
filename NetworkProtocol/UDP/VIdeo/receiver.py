# -*- coding: utf-8 -*-
import socket
import time
import cv2
import pickle
import numpy as np
import struct ## new

HOST='127.0.0.1'
PORT=8089

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind((HOST,PORT))
print ('Socket now listening')
s.connect(('127.0.0.1',8090))


### new
sdata = b""
data = b''
payload_size = struct.calcsize("L") 


while True:
    while len(data) < payload_size:
        data,addr = s.recvfrom(65535)
        if struct.unpack("L", data[:payload_size])[0] != 2764964:
            data = b""
            continue
         
 
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0]
    i = 0
    sig = 0
    while len(sdata) < msg_size:
        data,addr = s.recvfrom(61440)
        sdata += data
        i += 1
        if len(data) == 4:
            sig = 1
            break
        
    frame_data = sdata[:msg_size]
    sdata = b""
    data = b''
    ###
    if sig == 0:
        frame=pickle.loads(frame_data)
        cv2.imshow('frame',frame)
        cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
time2 = time.time()
