# -*- coding: utf-8 -*-
from tkinter import Button,PhotoImage,DoubleVar,OptionMenu,Label,NW
from tkinter.ttk import Progressbar
#import PIL
from PIL import Image, ImageTk
from struct import calcsize, unpack
from pickle import loads
from threading import Thread
from time import sleep
from socket import socket, AF_INET, SOCK_STREAM
from math import floor
from cv2 import cvtColor, COLOR_BGR2RGB
from contactTool import connectToAvailiblePort
import globalvar

class PlayFunction:
    def __init__(self, frame, style):
        super().__init__()
        self.style = style
        self.frame = frame
        self.playFlag = 0
        self.stopFlag = 0
        self.updatingID = 0
        self.speed = 1
        self.recvThread = 0
        self.updateThread = 0
        
        self.video_time()
        self.pauseimg = PhotoImage(file = "./icon/pause.png")
        self.pauseButton = Button(frame, image = self.pauseimg, relief = "flat", command = self.pause)
        self.playimg = PhotoImage(file = "./icon/play.png")
        self.playButton = Button(frame, image = self.playimg, relief = "flat", command = self.play)
     #   self.liveimg = PhotoImage(file = "./icon/live.png")
     #   self.liveButton = Button(frame, image = self.liveimg, relief = "flat")
     #   self.liveButton.place(x = 10, y = 10)
        self.pauseButton.place(x = 570, y = 650)
        
    
        self.speedlist(self.frame)
        
    def play(self):
        self.playFlag = 0
        self.playButton.place_forget()
        self.pauseButton.place(x = 570, y = 650)
    
    def pause(self):
        self.playFlag = 1
        self.pauseButton.place_forget()
        self.playButton.place(x = 570, y = 650)
        
    def play_video(self, notebook, count, canvas, root):
        self.stop_flag = 1
        notebook.select(0)
        
        if self.updatingID != 0:
            root.after_cancel(self.updatingID)
            self.recvThread.join()
            self.updateThread.join()
        sleep(3)
        
        self.stop_flag = 0
        self.recvThread = Thread(target = self.recv_frame)
        self.updateThread = Thread(target = self.update_frame,args = (canvas,root,self.speed))

        self.recvThread.start()
        sleep(1)
        self.updateThread.start()
        
    def update_frame(self, canvas, root, speed):
        if self.stop_flag == 0:
            frame = frames[0]
            frame = cvtColor(frame, COLOR_BGR2RGB)
            global photo
            photo = ImageTk.PhotoImage(image = Image.fromarray(frame))
            print(type(photo))
            canvas.create_image(0, 100, image = photo, anchor = NW)
            if self.playFlag == 0:
                del frames[0]
            self.updatingID = root.after(floor(23*(1/speed)),
                                          lambda : self.update_frame(canvas,root,self.speed))

    def recv_frame(self):
        print("start")
        data = b""
        payload_size = calcsize("L")
        global frames
        frames = []
        
        s=socket(AF_INET,SOCK_STREAM)
        connectToAvailiblePort(s,5000)
            
        
        s.sendall((globalvar.video_name).encode())
        while True:
            if self.stopFlag == 0:
                while len(data) < payload_size:
                    data += s.recv(4096)
            
                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = unpack("L", packed_msg_size)[0]
                while len(data) < msg_size:
                    data += s.recv(65536)
            
                frame_data = data[:msg_size] 
                data = data[msg_size:]
                frame= loads(frame_data)
                frames.append(frame)
                while len(frames) > 500:
                    sleep(0.01)
                s.sendall("resume".encode())
                
            else:
                s.sendall("restart".encode())
                sleep(0.5)
                s.close()
                break
            
    def changespeed(self, var, event):
        print(var.get())
        self.speed = var.get()
    
    def speedlist(self, root):
        speeds = [0.5,0.75,1,1.5,2]
        var = DoubleVar()
        var.set(speeds[2])
        speed_label = Label(root,text = "Speed: ",font = "times 20 bold")
        optionmenu = OptionMenu(root, var, *speeds,command = lambda event : self.changespeed(var,event))
        speed_label.place(x = 990,y = 608)
        optionmenu.place(x = 1080 ,y = 610)
        
    def video_time(self):
        self.style.configure("TProgressbar", foreground='blue', background='blue')
        bar = Progressbar(self.frame,value = 0,maximum = 100,length = 300,style = "TProgressbar")
        bar.place(x = 440, y = 630)
         