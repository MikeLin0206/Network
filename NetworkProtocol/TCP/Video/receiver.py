# -*- coding: utf-8 -*-
import socket
import time
import cv2
import pickle
import numpy as np
import struct ## new

HOST=''
PORT=8089

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('localhost',8089))

### new
data = b""
payload_size = struct.calcsize("L") 
print(payload_size)
time1 = time.time()
while True:
    while len(data) < payload_size:
        data += s.recv(4096)
        
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0]
    
    i = 0
    while len(data) < msg_size:
        data += s.recv(65536)
        i += 1
    frame_data = data[:msg_size]
    data = data[msg_size:]
    ###
    frame=pickle.loads(frame_data)
    #print(frame)
    cv2.imshow('frame',frame)
 #   print("test")
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
time2 = time.time()
print(time2 - time1)