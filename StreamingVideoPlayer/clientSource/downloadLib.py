# -*- coding: utf-8 -*-
from tkinter import Label, Toplevel, messagebox
from tkinter.ttk import Style, Progressbar
from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM
from contactTool import connectToAvailiblePort
from math import floor
import globalvar


class Download:
    def __init__(self):
        self.video_name = globalvar.video_name

    def download(self):
        s = Style()
        s.configure("TProgressbar", foreground='lightgreen', background='lightgreen')

        downloadPage = Toplevel()
        downloadPage.title("Download")
        downloadPage.geometry("350x200")
        label = Label(downloadPage,text = "{} is downloading...".format(globalvar.video_name))
        label.pack(pady = 20)
        bar = Progressbar(downloadPage, value = 0, maximum = 100, length = 300, style = "TProgressbar")
        bar.pack(pady = 40)

        downloadThread = Thread(target = self.downloadVideo, args = (bar, downloadPage))
        downloadThread.start()
    
    def downloadVideo(self, bar, page):
        sock = socket(AF_INET, SOCK_STREAM)
        connectToAvailiblePort(sock, 5002)
        sock.sendall(globalvar.video_name.encode())
        
        imgFile = open("test_" + globalvar.video_name, 'wb')
        total = int(globalvar.video_size.split(" ")[0])
        forward = floor(total / 100) * 1000
        count = 0
        progress = 0
        
        while True:
            imgData = sock.recv(1024)
            if not imgData:
                break
            
            imgFile.write(imgData)
            print(len(imgData))
            count += 1
            if count == forward:
                progress += 1
                bar['value']  = progress
                print(bar['value'])
                page.update()
                count = 0
                
        imgFile.close()
        sock.close()
        page.destroy()
        messagebox.showinfo("Finish","Video has downloaded")