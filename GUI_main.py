import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from subprocess import Popen

# Define the custom StylishButton class
class StylishButton(tk.Canvas):
    def __init__(self, master, text="", command=None, width=220, height=55,
                 font=('lato', 12, 'bold'), **kwargs):  # Updated font and size
        super().__init__(master, width=width, height=height, highlightthickness=0, bg="#66879C", bd=0, **kwargs)
        self.command = command
        self.text = text
        self.font = font
        self.width = width
        self.height = height
        self.radius = 20

        self.bg_color = "#DEE0ED"  # matches background
        self.border_color = "#88C7CE"
        self.hover_color = "#AC90F6"
        self.shadow_color = "#B0B0B0"
        self.text_color = "#1b1c1b"

        self.create_button()
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)

    def create_button(self, hover=False):
        self.delete("all")

        x0, y0, x1, y1 = 5, 5, self.width, self.height
        border_color = self.hover_color if hover else self.border_color
        text_offset = -1 if hover else 0

        # Draw shadow
        self.create_rounded_rect(x0+2, y0+2, x1+2, y1+2, self.radius, fill=self.shadow_color)

        # Draw button
        self.create_rounded_rect(x0, y0, x1, y1, self.radius, fill=self.bg_color, outline=border_color, width=2)

        # Add text
        self.create_text((self.width)//2, (self.height)//2 + text_offset, text=self.text, font=self.font, fill=self.text_color)

    def create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def on_enter(self, event):
        self.create_button(hover=True)
        self.configure(cursor='hand2')

    def on_leave(self, event):
        self.create_button(hover=False)

    def on_click(self, event):
        if self.command:
            self.command()


# Main Application Setup
root = tk.Tk()
root.title("HomePage")
root.geometry("1600x900")
root.configure(background="#DEE0ED")

# Get screen dimensions
w, h = root.winfo_screenwidth(), root.winfo_screenheight()

# Set up the background image and send it to the back
bg_image = Image.open('yoga.jfif').resize((w, h), Image.Resampling.LANCZOS)
background_image = ImageTk.PhotoImage(bg_image)
background_label = tk.Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
background_label.lower()  # Ensure background is behind other widgets

# Create header label with updated styling
header_label = tk.Label(root, text="Yoga Pose Detection Using Machine Learning",
                        font=("Times New Roman", 35, "bold"),
                        pady=12,
                        background="#AC90F6",
                        fg="black",
                        width=60,
                        borderwidth=8,
                        relief="raised",
                        height=1)
header_label.place(x=0, y=5)

# Create a vertical frame on the left side for buttons
side_button_frame = tk.Frame(root, bg="#66879C")
side_button_frame.place(x=50, y=200)  # Adjust X and Y to move vertically and horizontally

# Functions to open other pages
def open_login():
    root.withdraw()
    Popen(["python", "login.py"])

def open_register():
    root.destroy()
    Popen(["python", "registration.py"])

def open_tips():
    root.destroy()
    Popen(["python", "precautions.py"])
    
def start_pose_timer():
    from subprocess import call
    call(["python", "pose_timer_app.py"])
    
# def start_pose_timer():
#     #from subprocess import call
#     root.destroy()
#     Popen(["python", "pose_timer.py"])

def exit_app():
    root.destroy()

# Add vertical stylish buttons to the frame
btn_login = StylishButton(side_button_frame, text="Login", command=open_login)
btn_login.pack(pady=10)

btn_register = StylishButton(side_button_frame, text="Register", command=open_register)
btn_register.pack(pady=10)

btn_tips = StylishButton(side_button_frame, text="Tips", command=open_tips)
btn_tips.pack(pady=10)

btn_posetimer = tk.Button(root, text="Consistency Timer Mode", command=start_pose_timer)
btn_posetimer.pack(pady=10)

# btn_tips = StylishButton(side_button_frame, text="Pose Timer", command=open_tips)
# btn_tips.pack(pady=10)

btn_exit = StylishButton(side_button_frame, text="Exit", command=exit_app)
btn_exit.pack(pady=10)

watermark = tk.Label(
    root,
    text="© NBNSTIC COMP 2025",
    font=("Segoe UI", 10, "italic"),
    fg="#555555",      # Dark grey color
   # bg=root["background"]  # Inherits the window background
)
watermark.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)

root.mainloop()
