import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
import time

# Text content for yoga info tabs
DEFINITION_TEXT = (
    "Yoga poses, also known as asanas, are physical postures with ancient roots in Indian meditation practices. "
    "Originally developed to prepare the body for meditation, asanas today serve as a form of exercise that enhances "
    "flexibility, strength, balance, and mental well-being. In modern practice, they are central to Hatha yoga and are used "
    "for fitness, stress relief, and complementary therapies."
)

HISTORY_TEXT = (
    "The origins of yoga poses date back thousands of years in ancient India. Early texts, such as the Yoga Sutras of Patanjali, "
    "described asanas as 'steady and comfortable' postures primarily for meditation. Over time, the practice evolved from a spiritual "
    "discipline to a comprehensive system of physical and mental exercise. In the 20th century, pioneers like Yogendra, Kuvalayananda, "
    "and later B.K.S. Iyengar modernized these practices, making them accessible worldwide."
)

BENEFITS_TEXT = (
    "Modern research shows a range of benefits from practicing yoga poses:\n\n"
    "• Improved flexibility, muscle strength, and balance.\n"
    "• Enhanced posture and body awareness.\n"
    "• Reduced stress, anxiety, and depression through controlled breathing and mindfulness.\n"
    "• Relief for chronic conditions such as lower back pain and hypertension.\n\n"
    "Additionally, yoga may promote better sleep, cardiovascular health, and overall quality of life by integrating physical activity "
    "with mental focus and relaxation."
)

class YogaInfoPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg="seashell2")
        
         #Before commented from this
        header_frame = tk.Frame(self, bg="#6A1B9A", height=80)
        header_frame.pack(fill=tk.X)

        header_label = tk.Label(header_frame, text="Yoga Pose Information",
                                font=("Segoe UI", 20, "bold"),
                                bg="#6A1B9A", fg="white")
        header_label.pack(pady=20)
        
        #to this....

        # Tabbed interface for yoga content
        style = ttk.Style()
        style.configure("TNotebook.Tab",
                        font=("Segoe UI", 14, "bold"),
                        padding=[30, 10],
                        background="#D1C4E9",
                        foreground="black")
        style.map("TNotebook.Tab",
                  background=[("selected", "#9575CD")],
                  foreground=[("selected", "white")])

        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        def_tab = self.create_image_text_tab("yoga_definition.jpg", DEFINITION_TEXT)
        hist_tab = self.create_image_text_tab("yoga_history.jpg", HISTORY_TEXT)
        bene_tab = self.create_image_text_tab("yoga_benefits.jpg", BENEFITS_TEXT)

        notebook.add(def_tab, text="🧘 Definition")
        notebook.add(hist_tab, text="📜 History")
        notebook.add(bene_tab, text="💪 Benefits")

    def create_image_text_tab(self, image_file, content):
        frame = tk.Frame(self, bg="white")
        try:
            img = Image.open(image_file)
            img = img.resize((400, 200), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            img_label = tk.Label(frame, image=photo, bg="white")
            img_label.image = photo
            img_label.pack(pady=10)
        except Exception as e:
            print(f"Error loading {image_file}: {e}")

        text_widget = ScrolledText(frame, wrap=tk.WORD, font=("Segoe UI", 14), bg="white", fg="black")
        text_widget.insert(tk.END, content)
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        return frame

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Yoga Tracker App")
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{w}x{h}+0+0")
        self.configure(bg="seashell2")

        style = ttk.Style()
        style.theme_use("default")
        style.configure("TNotebook.Tab",
                        font=("Segoe UI", 14, "bold"),
                        padding=[30, 10],
                        background="#D1C4E9",
                        foreground="black")
        style.map("TNotebook.Tab",
                  background=[("selected", "#9575CD")],
                  foreground=[("selected", "white")])

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Add pages
        self.yoga_info_page = YogaInfoPage(self)
        self.notebook.add(self.yoga_info_page, text="🧘 Yoga Info")

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
