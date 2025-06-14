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

global fn
fn = ""
##############################################+=============================================================
root = tk.Tk()
root.configure(background="brown")
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
root.title("Yoga Pose Detection Using Machine Learning")

# ++++++++++++++++++++++++++++++++++++++++++++
#####For background Image
image2 = Image.open('a1.jpg')
image2 = image2.resize((1600, 1000),  Image.LANCZOS)
background_image = ImageTk.PhotoImage(image2)
background_label = tk.Label(root, image=background_image)
background_label.image = background_image
background_label.place(x=0, y=0)

# Updated Title label with new styling
label_l1 = tk.Label(root,
                    text="Yoga Pose Detection Using Machine Learning",
                    font=("Segoe UI", 28, 'bold'),
                    pady=12,
                    background="#AC90F6", fg="black", height=1)
label_l1.place(relx=0.5, y=5, anchor="n", relwidth=1)

def help():
    frame_alpr = tk.LabelFrame(root, text=" Yoga Poses ", width=1100, height=650, bd=0,
                               font=('times', 16, 'bold'), bg="#AC90F6")
    frame_alpr.grid(row=0, column=0, sticky='nw')
    frame_alpr.place(x=400, y=100)

    # Updated image size
    size = (250, 250)

    image3 = Image.open('v.jpg').resize(size, Image.LANCZOS)
    background_image3 = ImageTk.PhotoImage(image3)
    tk.Label(root, image=background_image3, text="Vajrasan", compound='bottom').place(x=430, y=130)
    
    image4 = Image.open('sar.jpg').resize(size, Image.LANCZOS)
    background_image4 = ImageTk.PhotoImage(image4)
    tk.Label(root, image=background_image4, text="Sarvangasan", compound='bottom').place(x=700, y=130)
    
    image5 = Image.open('shi.jpg').resize(size, Image.LANCZOS)
    background_image5 = ImageTk.PhotoImage(image5)
    tk.Label(root, image=background_image5, text="Shirsasan", compound='bottom').place(x=970, y=130)
    
    image6 = Image.open('ch.jpg').resize(size, Image.LANCZOS)
    background_image6 = ImageTk.PhotoImage(image6)
    tk.Label(root, image=background_image6, text="Chakrasan", compound='bottom').place(x=1240, y=130)
    
    image7 = Image.open('s.jpg').resize(size, Image.LANCZOS)
    background_image7 = ImageTk.PhotoImage(image7)
    tk.Label(root, image=background_image7, text="Shavasan", compound='bottom').place(x=430, y=420)
    
    image8 = Image.open('g.jpg').resize(size, Image.LANCZOS)
    background_image8 = ImageTk.PhotoImage(image8)
    tk.Label(root, image=background_image8, text="Gomukhaasan", compound='bottom').place(x=700, y=420)
    
    image9 = Image.open('b.jpg').resize(size, Image.LANCZOS)
    background_image9 = ImageTk.PhotoImage(image9)
    tk.Label(root, image=background_image9, text="Bhadraasan", compound='bottom').place(x=970, y=420)
    
    image10 = Image.open('d.jpg').resize(size, Image.LANCZOS)
    background_image10 = ImageTk.PhotoImage(image10)
    tk.Label(root, image=background_image10, text="Dhanurasan", compound='bottom').place(x=1240, y=420)

    # Prevent images from being garbage collected
    frame_alpr.image_refs = [background_image3, background_image4, background_image5,
                             background_image6, background_image7, background_image8,
                             background_image9, background_image10]






def action():
    from subprocess import call
    call(["python", "realtime_test.py"])

def pre():
    from subprocess import call
    call(["python", "precautions.py"])

def window():
    root.destroy()

# Updated buttons styling and spacing
button_y = 0.25
btn_height = 0.06
btn_gap = 0.08
btn_width = 0.2
btn_bg = "#AC90F6"
btn_fg = "black"
btn_font = ("times new roman", 16, "bold")

tk.Button(root, text="Precautions", command=pre, bd=0,
          background=btn_bg, foreground=btn_fg, font=btn_font).place(
          relx=0, rely=button_y, relwidth=btn_width, relheight=btn_height)

tk.Button(root, text="Recognize Yoga Pose", command=action, bd=0,
          background=btn_bg, foreground=btn_fg, font=btn_font).place(
          relx=0, rely=button_y + btn_gap, relwidth=btn_width, relheight=btn_height)

tk.Button(root, text="Help", command=help, bd=0,
          background=btn_bg, foreground=btn_fg, font=btn_font).place(
          relx=0, rely=button_y + 2*btn_gap, relwidth=btn_width, relheight=btn_height)

tk.Button(root, text="Exit", command=window, bd=0,
          background=btn_bg, foreground=btn_fg, font=btn_font).place(
          relx=0, rely=button_y + 3*btn_gap, relwidth=btn_width, relheight=btn_height)

              
# ... all your Home.py layout and widgets ...

# Add watermark at the bottom-right
# Watermark Label (bottom-right corner)
watermark = tk.Label(
    root,
    text='''Presented by -   
                 Shailendra Bhosale
                 Chirantan Chaudhari
                 Atharv Dabhade
                 Sairaj Deshmukh''',
    font=("Segoe UI", 10, "italic"),
    fg="#555555",      # Dark grey color
   # bg=root["background"]  # Inherits the window background
)
watermark.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)


root.mainloop()

