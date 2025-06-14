import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename
import cv2
import webbrowser

root = tk.Tk()
root.configure(background="#ECEFF1")
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
root.title("Yoga Pose Tips")

# Load and set background image
image2 = Image.open('yoga1.jpg').resize((w, h), Image.LANCZOS)
background_image = ImageTk.PhotoImage(image2)
background_label = tk.Label(root, image=background_image)
background_label.image = background_image
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Header with purple color
header_frame = tk.Frame(root, bg="#AC90F6", height=100)
header_frame.pack(fill=tk.X)

title_label = tk.Label(header_frame, text="Yoga Pose Detection Using Machine Learning",
                       font=("Tahoma", 24, 'bold'), bg="#AC90F6", fg="white")
title_label.pack(pady=20)

# Button bar
button_frame = tk.Frame(header_frame, bg="#AC90F6")
button_frame.pack()

def create_nav_button(text, command):
    return tk.Button(button_frame, text=text, command=command, width=17, height=2, bd=2,  # Added bd=2 for a thin border
                     font=('Verdana', 13, 'bold'), bg="#AC90F6", fg="white", activebackground="#9575CD", 
                     relief="solid")  # Added relief='solid' for a visible border


button1 = create_nav_button("Yoga Benefits", lambda: Fighting())
button2 = create_nav_button("What Is Yoga", lambda: WhatIsYoga())
button3 = create_nav_button("Types Of Yoga", lambda: TypesOfYoga())
button4 = create_nav_button("Morning Routine", lambda: Routine())
button5 = create_nav_button("Links Of Videos", lambda: vedio())

button1.grid(row=0, column=0, padx=10, pady=5)
button2.grid(row=0, column=1, padx=10, pady=5)
button3.grid(row=0, column=2, padx=10, pady=5)
button4.grid(row=0, column=3, padx=10, pady=5)
button5.grid(row=0, column=4, padx=10, pady=5)

# Functions to update content with header always on top
def show_background(image_path):
    image2 = Image.open(image_path).resize((w, h), Image.LANCZOS)
    background_image = ImageTk.PhotoImage(image2)
    bg_label = tk.Label(root, image=background_image)
    bg_label.image = background_image
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    header_frame.lift()

def update_label1(text):
    show_background("p2.jpg")
    result_label = tk.Label(root, text=text, width=40, font=("Verdana", 20, "bold"), bg='bisque2', fg='black')
    result_label.place(x=300, y=600)
    header_frame.lift()

def update_cal(text):
    result_label = tk.Label(root, text=text, width=40, font=("Verdana", 20, "bold"), bg='bisque2', fg='black')
    result_label.place(x=350, y=400)
    header_frame.lift()

# Redirect to benefits.py instead of changing image
def Fighting():
    from subprocess import call
    call(['python', 'benefits.py'])

def WhatIsYoga():
   from subprocess import call
   call(['python', 'whatisyoga.py'])

def TypesOfYoga():
    from subprocess import call
    call(['python', 'typesofyoga.py'])


def Routine():
    from subprocess import call
    call(['python', 'morningrutine.py'])

def vedio():
    from subprocess import call
    call(['python', 'videotutorials.py'])

root.mainloop()
