# -*- coding: utf-8 -*-
from socket import socket, AF_INET, SOCK_STREAM
import time
import struct
import pickle
import cv2
from serverTools import sendVideoList
import os
    
def download(host, port):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(1)
    
    connect, address = sock.accept()
    videoname = connect.recv(100)
    print(videoname.decode())
    imgFile = open(videoname.decode(), "rb")
    print("123")
    while True:
        imgData = imgFile.readline()
        if not imgData:
            break
        connect.send(imgData)
        
    imgFile.close()
    sock.close()
    connect.close()
    
    download(host, port)

def getComment(host, port):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(1)
 #   print("comment :",(host, port))
    connect,address = sock.accept()
    
    
    msg = connect.recv(1024)
    print(msg.decode())
    connect.sendall("Got it.Have a nice day!".encode())
    
    connect.close()
    sock.close()
    
    getComment(host, port)

def sending(host, port):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(1)
 #   print("sending :",(host, port))

    connect, address = sock.accept()
  #  sendVideoList(connect) 
    sentFrame = 0
    startTime = time.time()
    filename = connect.recv(100)
    cap=cv2.VideoCapture("./video/{}".format(filename.decode()))
   # print("./video/{}".format(filename.decode()))
   # print(os.getcwd())
  #  print(os.path.exists("./video/{}".format(filename.decode())))
   # 
    while True:
        rat, frame = cap.read()
        if not rat:
   #         print("test2")
            break
        frameData = pickle.dumps(frame)
        message_size = struct.pack("L", len(frameData))
        connect.sendall(message_size + frameData)
 #       print("test")
        msg = connect.recv(100)
        if msg.decode() == "restart": 
            break
    
        sentFrame += 1
        if sentFrame == 36 or sentFrame == 181 or sentFrame == 362:
            endTime = time.time()
            print("{:.4f}".format(endTime - startTime))

    connect.close()
    sock.close()
    
    sending(host, port)
    
def sendVodInfo(host, port):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(1)
    
    connect, address = sock.accept()
    sendVideoList(connect)
    
    sock.close()
    connect.close()
    
    sendVodInfo(host, port)