# -*- coding: utf-8 -*-
from threading import Thread
from serverThreads import download, getComment, sending
import os
  
host='127.0.0.1'
portIndex = 0
port = []
address = []

for i in range(0,30,3):
    port.append(5000 + i)
    address.append((host,port[portIndex]))
    portIndex += 1

#sendVodInfoThread = Thread(target = sendVodInfo, args = (host, 21025,))
#sendVodInfoThread.start()
#print(port)
#print(os.getcwd())
sendingThread = []
commentThread = []
downloadThread = []
for i in range(5):
    sendingThread.append(0)
    commentThread.append(0)
    downloadThread.append(0)
    
    sendingThread[i] = Thread(target = sending, args = (host, port[i],))
    commentThread[i] = Thread(target = getComment, args = (host, port[i] + 1,))
    downloadThread[i] = Thread(target = download, args = (host, port[i] + 2,))
    

    sendingThread[i].start()
    commentThread[i].start()
    downloadThread[i].start()
    