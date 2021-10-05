# -*- coding: utf-8 -*-
import cv2
import numpy as np
import socket
import time
import pickle
import struct

HOST='127.0.0.1'
PORT=8089
address = (HOST,PORT)

cap=cv2.VideoCapture("test3.mp4")
clientsocket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
clientsocket.bind(('127.0.0.1',8090))


cframe = 0
time1 = time.time()
while True:
    # Serialize frame
    rat,frame = cap.read()
    if not rat:
        break
    data = pickle.dumps(frame)
    message_size = struct.pack("L", len(data))
    for i in range(46):
        if i == 0:
            clientsocket.sendto(message_size,address)
            time.sleep(0.00001)
            clientsocket.sendto(data[i*61440:(i+1)*61440],address)
        else:
            clientsocket.sendto(data[i*61440:(i+1)*61440],address)
        time.sleep(0.00001)
    time.sleep(0.00001)

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