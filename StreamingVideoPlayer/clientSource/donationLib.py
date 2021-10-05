# -*- coding: utf-8 -*-
from tkinter import Toplevel, Label, Button, Entry, messagebox

class Donation():
    def __init__(self):
        self.card_num = []
        self.CVC = 0
    
    def donate(self):
        card = Toplevel()
        card.title("Card ceritification")
        card.geometry("350x200")
        Label(card,text = "Please enter your Visa and CVC:").pack()
        self.card_num = []
        for i in range(4):
            self.card_num.append(Entry(card,width = 4))
            self.card_num[i].place(x = 60 + i * 50,y = 40)
        self.CVC = Entry(card,width = 3)
        self.CVC.place(x = 300,y = 40)
        ok_button = Button(card,text = "OK",width = 5,command=lambda : self.check_card(card))
        ok_button.place(x = 210,y = 160)
        cancel_button = Button(card,text = "Cancel",width = 5,command = lambda : self.cancel(card))
        cancel_button.place(x = 280,y = 160)

    def check_card(self,card):
        sums = 0
        if len(self.CVC.get()) != 3:
            messagebox.showinfo("Invalid","CVC is wrong")
        else: 
            for i in range(4):
                if len(self.card_num[i].get()) != 4:
                    sums = 1
                    break
                for j in range(4):
                    if j % 2 == 0:
                        num = int(self.card_num[i].get()[j]) * 2
                    else:
                        num = int(self.card_num[i].get()[j])  
                    if num >= 10:
                        sums += int((num / 10)) + (num % 10) 
                    else:
                        sums += num
            print(sums)
            if sums % 10 == 0:
                card.destroy()
                self.enter_money()
            else:
                messagebox.showinfo("Invalid","The card is invalid")
        
    def enter_money(self):
        money = Toplevel()
        money.title("Donate")
        money.geometry("350x200")
        Label(money,text = "How much do you want to donate:").pack()
        dollor = Entry(money,width = 20)
        dollor.place(x = 80,y = 40)
        Label(money,text = "NTD").place(x = 260,y = 40)
        ok_button = Button(money,text = "OK",width = 5,command = lambda: self.donate_info(money,dollor))
        ok_button.place(x = 210,y = 160)
        cancel_button = Button(money,text = "Cancel",width = 5,command = lambda : self.cancel(money))
        cancel_button.place(x = 280,y = 160)
    
    def donate_info(self,window,dollor):
        messagebox.showinfo("Thanks","Thanks for your donate \r ${}!".format(dollor.get()))
        window.destroy()
    
    def cancel(self,window):
        window.destroy()