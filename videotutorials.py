import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import webbrowser

try:
    from tkvideo import tkvideo
except ImportError:
    tkvideo = None

videos = {
    "Sun Salutation": {
        "thumbnail": "2.jpg",
        "video": "sun_satulation.mp4",
        "description": "Energize your morning with the dynamic sequence of Sun Salutation."
    },
    "Warrior Sequence": {
        "thumbnail": "9.jpg",
        "video": "warrior.mp4",
        "description": "Build strength, focus, and balance with a complete Warrior Sequence."
    },
    "Morning Flow": {
        "thumbnail": "3.jpg",
        "video": "morning_yoga.mp4",
        "description": "A gentle flow to stretch and awaken your body for the day ahead."
    },
    "Sun Salutation": {
        "thumbnail": "2.jpg",
        "video": "sun_satulation.mp4",
        "description": "Energize your morning with the dynamic sequence of Sun Salutation."
    },
    "Warrior Sequence": {
        "thumbnail": "9.jpg",
        "video": "warrior.mp4",
        "description": "Build strength, focus, and balance with a complete Warrior Sequence."
    },
    "Morning Flow": {
        "thumbnail": "3.jpg",
        "video": "morning_yoga.mp4",
        "description": "A gentle flow to stretch and awaken your body for the day ahead."
    },
    "Balance & Flexibility": {
        "thumbnail": "4.jpg",
        "video": "flexibility.mp4",
        "description": "Improve your balance and flexibility through targeted yoga poses."
    },
    "Cool Down & Meditation": {
        "thumbnail": "7.jpg",
        "video": "meditation.mp4",
        "description": "Relax your mind and body with a cool down session followed by meditation."
    }
}

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, bg_color="seashell2", *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.bg_color = bg_color
        self.canvas = tk.Canvas(self, bg=bg_color, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=bg_color)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)
    
    def _on_mousewheel(self, event):
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")

class YogaVideoTutorialPage(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(bg="#ECEFF1")
        self.score = 0
        self.played_videos = set()
        
        header_frame = tk.Frame(self, bg="#AC90F6", height=120)
        header_frame.pack(fill=tk.X)
        header_title = tk.Label(header_frame, text="Yoga Video Tutorials",
                                font=("Tahoma", 24, "bold"), bg="#AC90F6", fg="white")
        header_title.pack(side=tk.LEFT, padx=20, pady=20)
        self.score_label = tk.Label(header_frame, text="Score: 0", font=("Tahoma", 20),
                                    bg="#AC90F6", fg="white")
        self.score_label.pack(side=tk.RIGHT, padx=20, pady=20)
        
        content_container = ScrollableFrame(self, bg_color="#ECEFF1")
        content_container.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        cards_frame = content_container.scrollable_frame
        columns = 3
        for idx, (title, data) in enumerate(videos.items()):
            shadow_frame = tk.Frame(cards_frame, bg="#757575")
            shadow_frame.grid(row=idx // columns, column=idx % columns, padx=15, pady=15, sticky="nsew")
            cards_frame.grid_columnconfigure(idx % columns, weight=1)
            cards_frame.grid_rowconfigure(idx // columns, weight=1)

            # Border frame simulates the border color
            border_frame = tk.Frame(shadow_frame, bg="#AC90F6", padx=3, pady=3)
            border_frame.pack(expand=True, fill="both")

            card = tk.Frame(border_frame, bg="white", bd=0, relief=tk.FLAT)
            card.pack(expand=True, fill="both")

            try:
                thumb_img = Image.open(data["thumbnail"])
                thumb_img = thumb_img.resize((300, 200), Image.LANCZOS)
                thumb_photo = ImageTk.PhotoImage(thumb_img)
            except Exception as e:
                print(f"Error loading {data['thumbnail']}: {e}")
                thumb_photo = None
            
            if thumb_photo:
                img_label = tk.Label(card, image=thumb_photo, bg="white", bd=0)
                img_label.image = thumb_photo
                img_label.pack(pady=(10, 5))
            
            title_label = tk.Label(card, text=title, font=("Verdana", 16, "bold"), bg="white", fg="#3F51B5")
            title_label.pack(pady=5)
            desc_label = tk.Label(card, text=data["description"], font=("Arial", 12), bg="white",
                                  wraplength=280, justify=tk.LEFT)
            desc_label.pack(padx=10, pady=5)
            
            play_btn = tk.Button(card, text="Play ▶", font=("Verdana", 12, "bold"),
                                 bg="#FF5722", fg="white", bd=0, activebackground="#E64A19",
                                 command=lambda t=title, d=data: self.open_video_popup(t, d))
            play_btn.pack(pady=10)
    
    def open_video_popup(self, title, video_data):
        if title not in self.played_videos:
            self.played_videos.add(title)
            self.score += 10
            self.score_label.config(text=f"Score: {self.score}")
            if self.score >= 50:
                messagebox.showinfo("Achievement Unlocked!",
                                    "Great job! You've earned a badge for watching multiple tutorials!")
        
        popup = tk.Toplevel(self)
        popup.title(title)
        popup.configure(bg="black")
        popup.geometry("800x450")
        
        if tkvideo:
            try:
                video_label = tk.Label(popup, bg="black")
                video_label.pack(expand=True, fill=tk.BOTH)
                player = tkvideo(video_data["video"], video_label, loop=1, size=(800, 450))
                player.play()
            except Exception as e:
                error_label = tk.Label(popup, text="Error playing video.",
                                       font=("Tahoma", 16), bg="black", fg="white")
                error_label.pack(expand=True)
        else:
            msg = ("Video playback is not available in-app.\n"
                   "Click the button below to open the video in your web browser.")
            msg_label = tk.Label(popup, text=msg, font=("Tahoma", 16), bg="black", fg="white")
            msg_label.pack(expand=True, pady=20)
            open_link = tk.Button(popup, text="Open Video", font=("Tahoma", 16, "bold"),
                                  bg="#FF5722", fg="white", bd=0, activebackground="#E64A19",
                                  command=lambda: webbrowser.open(video_data["video"]))
            open_link.pack(pady=50)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Yoga Video Tutorials")
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry("%dx%d+0+0" % (w, h))
    
    video_page = YogaVideoTutorialPage(root)
    video_page.pack(expand=True, fill=tk.BOTH)
    
    root.mainloop()
