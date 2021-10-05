# -*- coding: utf-8 -*-
from tkinter import END
import globalvar


def treeInsert(tree,mode):
    sportlist = [["test.mp4","6:55","203 MB"],["test2.mp4","13:28","130 MB"]]
    serieslist = ["test.mp4","test2.mp4"] 
    movielist = ["test.mp4","test2.mp4"]
    category = [sportlist,serieslist,movielist]
    for i in category[mode]:
        tree.insert("",index = END,value =(i[0].split(".")[0],i[1] ,i[2]),tags = "Color")
        
def treeSelect(event):
    widgetObj = event.widget
    itemselected = widgetObj.selection()
    child = widgetObj.get_children()
    for i in child:
        widgetObj.item(i,tags = "Color")
    widgetObj.item(itemselected,tags = "SelectColor")
    globalvar.video_name = widgetObj.item(itemselected,"values")[0] + ".mp4"
    globalvar.video_length = widgetObj.item(itemselected,"values")[1]
    globalvar.video_size = widgetObj.item(itemselected,"values")[2]