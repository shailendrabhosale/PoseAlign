import tkinter as tk
from tkinter import messagebox
import sqlite3
from subprocess import Popen

# -----------------------
# Rounded Border Canvas Class
# -----------------------
class RoundedContainer(tk.Canvas):
    def __init__(self, parent, width, height, radius=20, border_color="#800080", fill="#FFF4E5", **kwargs):
        super().__init__(parent, width=width, height=height, bg=fill, highlightthickness=0, **kwargs)
        self.radius = radius
        self.border_color = border_color
        self.fill = fill
        self.rounded_rect(width, height)

    def rounded_rect(self, w, h):
        r = self.radius
        # Draw outer arcs and lines to simulate a thin thread-like purple border
        self.create_arc((0, 0, 2*r, 2*r), start=90, extent=90, outline=self.border_color, style="arc", width=2)
        self.create_arc((w-2*r, 0, w, 2*r), start=0, extent=90, outline=self.border_color, style="arc", width=2)
        self.create_arc((0, h-2*r, 2*r, h), start=180, extent=90, outline=self.border_color, style="arc", width=2)
        self.create_arc((w-2*r, h-2*r, w, h), start=270, extent=90, outline=self.border_color, style="arc", width=2)
        self.create_line((r, 0, w-r, 0), fill=self.border_color, width=2)
        self.create_line((r, h, w-r, h), fill=self.border_color, width=2)
        self.create_line((0, r, 0, h-r), fill=self.border_color, width=2)
        self.create_line((w, r, w, h-r), fill=self.border_color, width=2)


# -----------------------
# Main Window Setup
# -----------------------
window = tk.Tk()
window.title("Register")
window.configure(bg="#FFF4E5")
w, h = window.winfo_screenwidth(), window.winfo_screenheight()
window.geometry(f"{w}x{h}+0+0")

# -----------------------
# Heading Label (Full width)
# -----------------------
label_l1 = tk.Label(window,
                    text="Yoga Pose Detection Using Machine Learning",
                    font=("Segoe UI", 28, 'bold'),  # Reduced font size
                    pady=12,
                    background="#AC90F6", fg="black", height=1)
label_l1.place(relx=0.5, y=5, anchor="n", relwidth=1)  # Full width of the screen

# -----------------------
# Variables
# -----------------------
Fullname = tk.StringVar()
username = tk.StringVar()
Email = tk.StringVar()
password = tk.StringVar()
password1 = tk.StringVar()

# -----------------------
# Fonts
# -----------------------
title_font = ("Segoe UI", 22, "bold")  # Reduced font size for the title
label_font = ("Segoe UI", 14)  # Smaller font size for labels
entry_font = ("Segoe UI", 14)
button_font = ("Segoe UI", 14, "bold")

# -----------------------
# Create Rounded Canvas
# -----------------------
container_width = 600
container_height = 500

rounded = RoundedContainer(window, width=container_width, height=container_height, radius=25)
rounded.place(relx=0.5, rely=0.5, anchor="center")

# -----------------------
# Frame Inside Rounded Container
# -----------------------
frame = tk.Frame(rounded, bg="#FFF4E5")
frame.place(x=20, y=20, width=container_width - 40, height=container_height - 40)

tk.Label(frame, text="Create Account", font=title_font, bg="#FFF4E5", fg="#333333").grid(row=0, column=0, columnspan=2, pady=(0, 30))

# -----------------------
# Form Fields
# -----------------------
def create_label_entry(text, var, row, show=None):
    label = tk.Label(frame, text=text, font=label_font, bg="#FFF4E5", fg="#333333", anchor="w", width=16)
    label.grid(row=row, column=0, sticky="w", padx=(0, 10), pady=10)

    entry = tk.Entry(frame, textvariable=var, font=entry_font, bd=2, width=30, show=show)
    entry.grid(row=row, column=1, sticky="e", padx=(0, 10), pady=10)

create_label_entry("Full Name", Fullname, 1)
create_label_entry("Username", username, 2)
create_label_entry("Email", Email, 3)
create_label_entry("Password", password, 4, show="*")
create_label_entry("Confirm Password", password1, 5, show="*")

# -----------------------
# Register Logic
# -----------------------
def insert():
    fname = Fullname.get()
    un = username.get()
    email = Email.get()
    pwd = password.get()
    cnpwd = password1.get()

    if not fname or not un or not email or not pwd:
        messagebox.showerror("Error", "All fields are required!")
        return
    if pwd != cnpwd:
        messagebox.showerror("Error", "Passwords do not match!")
        return

    with sqlite3.connect('evaluation.db') as db:
        cursor = db.cursor()
        cursor.execute('INSERT INTO registration (Fullname, username, Email, password) VALUES (?, ?, ?, ?)',
                       (fname, un, email, pwd))
        db.commit()
        messagebox.showinfo("Success", "Registration successful!")
        window.destroy()
        Popen(["python", "login.py"])

# -----------------------
# Buttons
# -----------------------
button_frame = tk.Frame(frame, bg="#FFF4E5")
button_frame.grid(row=6, column=0, columnspan=2, pady=20)

tk.Button(button_frame, text="Back to Login",
          command=lambda: [window.destroy(), Popen(["python", "login.py"])],
          font=button_font, bg="#AC90F6", fg="#FFFFFF", padx=20, pady=8, bd=0).grid(row=0, column=0, padx=10)

tk.Button(button_frame, text="Register", command=insert,
          font=button_font, bg="#AC90F6", fg="#FFFFFF", padx=20, pady=8, bd=0).grid(row=0, column=1, padx=10)

window.mainloop()
