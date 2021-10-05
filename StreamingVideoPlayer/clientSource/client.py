# -*- coding: utf-8 -*-
from tkinter import Canvas,Tk,Frame,Button,Label,Text, E, W
from tkinter.ttk import Notebook,Style,Treeview
import globalvar
import client_func
from buildTree import treeInsert, treeSelect
from contactTool import sendMsg#, getVODInfo
from donationLib import Donation
from downloadLib import Download

host = "127.0.0.1"

globalvar.init()
root = Tk()
root.title("video")
root.geometry("1200x800")

#vodInfo = getVODInfo(host, 21025)

####Make style
style = Style()
style.theme_create( "TabStyle",parent="clam", settings={
                    "TNotebook.Tab": {"configure": {"padding": [167, 10],
                                      "font"     : ('URW Gothic L', '11', 'bold')},}})
style.theme_use("TabStyle")
style.configure("TProgressbar", foreground='green', background='green')
####Make style

####Create Notebook
notebook = Notebook()
play_frame = Frame()
video_frame = Frame()
contact_frame = Frame()
notebook.add(play_frame, text = "Watch")
notebook.add(video_frame,text = "Videos")
notebook.add(contact_frame,text = "Contact us")
notebook.grid(padx=10, pady=10)

canvas = Canvas(play_frame, width = 720, height = 580)
#canvas.pack()
canvas.place(x = 240, y = 30)
####Create Notebook

####Function object
playing_video = client_func.PlayFunction(play_frame,style)
donation = Donation()
download = Download()
####Function object

####Video select
videoPage = Notebook(video_frame)
sport_frame = Frame()
series_frame = Frame()
movie_frame = Frame()
videoPage.add(sport_frame ,text = "Sport")
videoPage.add(series_frame , text = "Series")
videoPage.add(movie_frame , text = "Movie")
videoPage.grid(padx = 10,pady = 10)

trees = ["sport_tree","series_tree","movie_tree"]
video_frames = [sport_frame,series_frame,movie_frame]
for i in range(3):
    select_button = Button(video_frames[i],text = "Play",font = "times 30 bold",
                           command = lambda : playing_video.play_video(notebook,0,canvas,root))
    download_button = Button(video_frames[i],text = "Download",command = download.download)
    trees[i] = Treeview(video_frames[i],columns = ("name","length","size"),show='headings',selectmode="browse")
    trees[i].column("#1",anchor='center')
    trees[i].column("#2",anchor='center')
    trees[i].column("#3",anchor='center')
    trees[i].heading("#1", text = "Name")
    trees[i].heading("#2", text = "Length")
    trees[i].heading("#3", text = "Size")
    trees[i].grid(padx = 280,pady = 50)
    trees[i].tag_configure("Color", background="white")
    trees[i].tag_configure("SelectColor", background="lightblue")
    treeInsert(trees[i],i)
    trees[i].bind("<<TreeviewSelect>>", treeSelect)
    trees[i].bind("<Double-1>",lambda x : playing_video.play_video(notebook,0,canvas,root,))
    select_button.grid(pady = 20)
    download_button.grid(pady = 20,padx = 20,sticky = "E")
####Video select

####Contact server
message_label = Label(contact_frame,text = "Have any comment or advise?"
                                            ,font = "times 20")
message_label.grid(padx = 400,pady = 70)
contact_text = Text(contact_frame,width = 100,height = 10)
contact_text.grid()
send_button = Button(contact_frame,text = "Send",font = "times 20 bold",
                     command = lambda : sendMsg(contact_text))
send_button.grid(pady = 30)
mail_label = Label(contact_frame,text = "Email:lab409@gmail.com")
mail_label.grid(row = 4,sticky = "ws",padx = 35)
donate_button = Button(contact_frame,text = "Donate",font = "times 30 bold",
                       fg = "Yellow",bg="Green",command = donation.donate)
donate_button.grid(row = 4,sticky = "ws",padx = 50,pady = 100)
####Contact server

videoPage.mainloop()
notebook.mainloop()
root.mainloop()

