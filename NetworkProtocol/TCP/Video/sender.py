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

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
cap=cv2.VideoCapture("test3.mp4")
s.bind((HOST,PORT))
s.listen(10)

conn,addr=s.accept()
cframe = 0
time1 = time.time()
while True:
    # Serialize frame
    rat,frame = cap.read()
    if not rat:
        break
    data = pickle.dumps(frame)
    message_size = struct.pack("L", len(data))
    conn.sendall(message_size + data)

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

print(cframe)
time2 = time.time()
print(time1 - time2)

