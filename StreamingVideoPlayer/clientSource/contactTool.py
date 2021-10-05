# -*- coding: utf-8 -*-
from socket import socket, AF_INET, SOCK_STREAM
from tkinter import END, messagebox


def sendMsg(text):
    sock = socket(AF_INET, SOCK_STREAM)  
    connectToAvailiblePort(sock, 5001)
    msg = text.get(1.0, END)
    sock.sendall(msg.encode())
    recvMsg = sock.recv(100)
    messagebox.showinfo("Server got your message!", recvMsg.decode())
    
    text.delete(1.0,END)
    
def connectToAvailiblePort(socket,port):
    for i in range(10):
        try:
            socket.connect(('127.0.0.1',port))
            break
        except:
            port += 3

def getVODInfo(host, port):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((host, port))
    
    data = sock.recv(65535)
    data = data.decode("utf-8")
    
    sock.close()
    
    return data