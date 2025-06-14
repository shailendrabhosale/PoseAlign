# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 14:45:37 2024

@author: admin
"""
# Import Module 
import tkinter as tk
from tkinter import ttk, LEFT, END
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox as ms
import cv2
import sqlite3
import os
import numpy as np
import time
import webbrowser
global fn
fn = ""
##############################################+=============================================================
root = tk.Tk()
root.configure(background="brown")
# root.geometry("1300x700")


w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
root.title("Yoga Pose Detection Using Machine Learning")

# 43

# ++++++++++++++++++++++++++++++++++++++++++++
#####For background Image
image2 = Image.open('yoga5.webp')
image2 = image2.resize((1600, 1000), Image.ANTIALIAS)

background_image = ImageTk.PhotoImage(image2)

background_label = tk.Label(root, image=background_image)

background_label.image = background_image

background_label.place(x=0, y=0)  # , relwidth=1, relheight=1)
#
label_l1 = tk.Label(root, text="Yoga Pose Detection Using Machine Learning",font=("Times New Roman", 35, 'bold'),
                    background="#607D86", fg="black", width=60, height=1)
label_l1.place(x=0, y=0)


################################$%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



my_link=tk.Label(root,text='Vajrasan',bg="#607D86",fg="white",width=15,cursor='hand2',height=1,font=("Times", 20, 'underline'))
my_link.place(x=0,y=100)
# grid(padx=400,pady=10)

my_link.bind('<Button-1>',
lambda x:webbrowser.open_new("https://youtu.be/fSKBk9u9tP8"))


my_link2=tk.Label(root,text='Sarvangasana',bg="#607D86",fg="white",cursor='hand2',width=15,height=1,font=("Times", 20, 'underline'))
my_link2.place(x=0,y=200)

my_link2.bind('<Button-1>',
    lambda x:webbrowser.open_new("https://youtu.be/g3wvIPXZ-Qo"))    
   
my_link2=tk.Label(root,text='Gomukhasana',bg="#607D86",fg="white",cursor='hand2',width=15,height=1,font=("Times", 20, 'underline'))
my_link2.place(x=0,y=300)

my_link2.bind('<Button-1>',
    lambda x:webbrowser.open_new("https://youtu.be/d_dh_DwDr84")) 


my_link2=tk.Label(root,text='Bhadrasana',bg="#607D86",fg="white",cursor='hand2',width=15,height=1,font=("Times", 20, 'underline'))
my_link2.place(x=0,y=400)

my_link2.bind('<Button-1>',
    lambda x:webbrowser.open_new("https://youtu.be/ndfx530PNuI"))

my_link2=tk.Label(root,text='Shavasana',bg="#607D86",fg="white",cursor='hand2',width=15,height=1,font=("Times", 20, 'underline'))
my_link2.place(x=0,y=500)

my_link2.bind('<Button-1>',
    lambda x:webbrowser.open_new("https://youtu.be/SfAoPVt64LE"))

my_link2=tk.Label(root,text='Shavasana',bg="#607D86",fg="white",cursor='hand2',width=15,height=1,font=("Times", 20, 'underline'))
my_link2.place(x=0,y=600)

my_link2.bind('<Button-1>',
    lambda x:webbrowser.open_new("https://youtu.be/-pebIpb4dOE"))

my_link2=tk.Label(root,text='Shirsana',bg="#607D86",fg="white",cursor='hand2',width=15,height=1,font=("Times", 20, 'underline'))
my_link2.place(x=0,y=600)

my_link2.bind('<Button-1>',
    lambda x:webbrowser.open_new("https://www.youtube.com/shorts/QNTnBisZRP8?feature=share"))
#################################################################################################################
def window():
    root.destroy()

# button3=tk.Button(root,text="Recognize Yoga Pose",command=action,width=20,height=2,bd=0,background="#C0C2D1",foreground="black",font=("times new roman",14,"bold"))
# button3.place(x=100,y=220)



root.mainloop()