import tkinter as tk
from tkinter import messagebox as ms
import sqlite3
from PIL import Image, ImageTk, ImageDraw, ImageFilter
from subprocess import Popen

# -----------------------
# GlassFrame: A custom canvas that draws a rounded, glassy panel with shadow
# -----------------------
class GlassFrame(tk.Canvas):
    def __init__(self, parent, width, height, corner_radius=20, shadow_offset=10, **kwargs):
        super().__init__(parent, width=width, height=height, highlightthickness=0, bd=0, **kwargs)
        self.width = width
        self.height = height
        self.corner_radius = corner_radius
        self.shadow_offset = shadow_offset
        self.configure(bg=parent["background"])
        self.create_glass_effect()

    def create_glass_effect(self):
        # Create an RGBA image for glass effect
        img = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Shadow
        shadow = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow)
        rect = [self.shadow_offset, self.shadow_offset, self.width - self.shadow_offset, self.height - self.shadow_offset]
        shadow_draw.rounded_rectangle(rect, radius=self.corner_radius, fill=(0, 0, 0, 80))
        shadow = shadow.filter(ImageFilter.GaussianBlur(5))
        img = Image.alpha_composite(img, shadow)

        # Transparent white with blur-style look (glass effect)
        glass_color = (255, 255, 255, 80)  # semi-transparent white
        main_rect = [0, 0, self.width - self.shadow_offset, self.height - self.shadow_offset]
        draw.rounded_rectangle(main_rect, radius=self.corner_radius, fill=glass_color)

        self.glass_img = ImageTk.PhotoImage(img)
        self.create_image(0, 0, anchor="nw", image=self.glass_img)

# -----------------------
# Main Application Setup
# -----------------------
root = tk.Tk()
root.configure(background="#FFF4E5")
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry(f"{w}x{h}+0+0")
root.title("Login Form")

# -----------------------
# Heading Label
# -----------------------
label_l1 = tk.Label(root,
                    text="Yoga Pose Detection Using Machine Learning",
                    font=("Segoe UI", 28, 'bold'),  # Reduced font size
                    pady=12,
                    background="#AC90F6", fg="black", height=1)
label_l1.place(relx=0.5, y=5, anchor="n", relwidth=1)  # Full width of the screen

# Login variables
username = tk.StringVar()
password = tk.StringVar()

# -----------------------
# Functions for Navigation and Login
# -----------------------
def open_main():
    root.destroy()
    Popen(["python", "registration.py"])

def login():
    with sqlite3.connect('evaluation.db') as db:
        c = db.cursor()
        find_entry = "SELECT * FROM registration WHERE username = ? AND password = ?"
        c.execute(find_entry, [username.get(), password.get()])
        result = c.fetchall()
        if result:
            ms.showinfo("Message", "Login Successful")
            root.destroy()
            Popen(["python", "Home.py"])
        else:
            ms.showerror("Error", "Invalid Username or Password")

# -----------------------
# Glass Frame for Login
# -----------------------
frame_width = 550
frame_height = 400
glass = GlassFrame(root, width=frame_width, height=frame_height, corner_radius=20, shadow_offset=10)
glass.place(x=(w - frame_width) // 2, y=250)

# -----------------------
# Transparent login frame on top of glass
# -----------------------
login_frame = tk.Frame(glass, bg="#FFFFFF", bd=0)
login_frame.place(x=20, y=20, width=frame_width - 40, height=frame_height - 40)
login_frame.configure(bg=root["background"])
login_frame.grid_columnconfigure(0, weight=1)
login_frame.grid_columnconfigure(1, weight=1)

# -----------------------
# Fonts
# -----------------------
title_font = ("Segoe UI", 18, "bold")
label_font = ("Segoe UI", 12)
entry_font = ("Segoe UI", 12)
button_font = ("Segoe UI", 12, "bold")

# -----------------------
# Login UI Elements
# -----------------------
title_label = tk.Label(login_frame, text="Login Here", font=title_font, bg=root["background"], fg="#222")
title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

username_label = tk.Label(login_frame, text="Username", font=label_font, bg=root["background"], fg="#333")
username_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
username_entry = tk.Entry(login_frame, textvariable=username, font=entry_font, bg="#F0F0F0", relief="sunken", bd=2)
username_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

password_label = tk.Label(login_frame, text="Password", font=label_font, bg=root["background"], fg="#333")
password_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
password_entry = tk.Entry(login_frame, textvariable=password, font=entry_font, show="*", bg="#F0F0F0", relief="sunken", bd=2)
password_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

# Buttons container frame to center horizontally
buttons_frame = tk.Frame(login_frame, bg=root["background"])
buttons_frame.grid(row=3, column=0, columnspan=2, pady=20)

login_button = tk.Button(buttons_frame, text="Login", command=login, font=button_font, bg="#AC90F6", fg="white", padx=15, pady=5, relief="flat")
login_button.pack(side="left", padx=20)

register_button = tk.Button(buttons_frame, text="Register", command=open_main, font=button_font, bg="#AC90F6", fg="white", padx=15, pady=5, relief="flat")
register_button.pack(side="left", padx=20)


watermark = tk.Label(
    root,
    text="© NBNSTIC COMP 2025",
    font=("Segoe UI", 10, "italic"),
    fg="#555555",      # Dark grey color
   # bg=root["background"]  # Inherits the window background
)
watermark.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)


root.mainloop()
