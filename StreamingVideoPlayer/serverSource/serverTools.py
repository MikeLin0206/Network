# -*- coding: utf-8 -*-
from socket import socket, AF_INET, SOCK_STREAM
from os import listdir, stat
from pymediainfo import MediaInfo

def sendVideoList(sock):
    videoList = getVideoInfo()
    sock.send(str(videoList).encode("utf-8"))

def getVideoInfo():
    resultList = []
    for file in listdir("./video"):
        info = stat("./video/{}".format(file))
        size = int(info.st_size / 1024 / 1024)
        
        media_info = MediaInfo.parse("./video/{}".format(file))
        duration = media_info.tracks[0].duration
        minute = int(duration / 1000 // 60)
        second = int(duration / 1000 % 60)
        result = [file, "{}:{}".format(minute, second), "{}MB".format(size)]
        resultList.append(result)
    return resultList