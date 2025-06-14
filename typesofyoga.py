import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk

# Yoga types content
YOGA_TYPES = {
    "Hatha Yoga": {
        "image": "2.jpg",
        "desc": "   Hatha Yoga is a traditional and foundational form of yoga that focuses on balancing the body and mind through physical postures (asanas), breathing techniques (pranayama), and relaxation. The word 'Hatha' combines 'Ha' (sun) and 'Tha' (moon), symbolizing energy and calmness. It's ideal for beginners due to its slow and gentle pace, helping improve flexibility, strength, focus, sleep, and overall health. Hatha Yoga also prepares the mind for deeper meditation by promoting inner peace and awareness.",
        "color": "#FFCCBC"
    },
    "Vinyasa Yoga": {
        "image": "3.jpg",
        "desc": "   Vinyasa Yoga is a dynamic and flowing style of yoga where movements are smoothly linked with breath, creating a dance-like sequence of poses. The word 'Vinyasa' means “to place in a special way,” highlighting the mindful transitions between postures. It builds strength, flexibility, and endurance, while also boosting focus and relieving stress. Often faster-paced than Hatha, Vinyasa is great for those who enjoy movement and want a full-body workout with mental calmness.",
        "color": "#B2EBF2"
    },
    "Ashtanga Yoga": {
        "image": "4.jpg",
        "desc": "   Ashtanga Yoga is a powerful, structured style of yoga that follows a specific sequence of poses linked by breath and movement. The word 'Ashtanga' means 'eight limbs', referring to eight steps toward spiritual growth, including posture, breath, and meditation. It's physically intense, builds strength, flexibility, and discipline, and is great for those who like routine and challenge. Ashtanga brings focus, inner balance, and deep body awareness.",
        "color": "#C5E1A5"
    },
    "Kundalini Yoga": {
        "image": "7.jpg",
        "desc": "   Kundalini Yoga is a spiritual and energetic form of yoga that focuses on awakening the dormant energy (Kundalini) at the base of the spine through a mix of poses, breathwork, chanting, and meditation. Its goal is to raise this energy upward through the chakras, leading to higher awareness and inner transformation. Kundalini Yoga boosts creativity, clarity, emotional balance, and spiritual connection, making it powerful for those seeking deep mental and spiritual growth.",
        "color": "#E1BEE7"
    },
    "Yin Yoga": {
        "image": "9.jpg",
        "desc": "   Yin Yoga is a slow, meditative style of yoga where poses are held for several minutes to gently stretch deep connective tissues like ligaments, joints, and fascia. It targets areas like hips, spine, and pelvis, improving flexibility and joint health. Yin encourages stillness, patience, and mindfulness, making it perfect for stress relief, inner calm, and balancing more active (yang) lifestyles.",
        "color": "#D7CCC8"
    },
    "Power Yoga": {
        "image": "11.jpg",
        "desc": "   Power Yoga is a vigorous, fast-paced style of yoga that combines strength-building poses with dynamic movements. It's based on Vinyasa but with more intensity, focusing on increasing muscle strength, flexibility, and endurance. Power Yoga boosts energy, enhances cardiovascular health ❤️, and helps burn calories, making it ideal for those looking for a challenging workout with the added benefits of mindfulness and stress relief.",
        "color": "#FFECB3"
    },
}


class YogaTypesComponent(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg="seashell2")

        # Header section
        header_frame = tk.Frame(self, bg="#6A1B9A", height=100)
        header_frame.pack(fill=tk.X)
        header_label = tk.Label(header_frame,
                                text="Types of Yoga",
                                font=("Tahoma", 24, "bold"),
                                bg="#6A1B9A", fg="white")
        header_label.pack(pady=20)

        # Notebook with colored tabs
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TNotebook.Tab",
                        font=("Segoe UI", 12, "bold"),  # Reduced font size from 14 to 12
                        padding=[15, 8],               # Adjusted padding to match font size
                        background="#D1C4E9",
                        foreground="black")
        style.map("TNotebook.Tab",
                  background=[("selected", "#9575CD")],
                  foreground=[("selected", "white")])

        notebook = ttk.Notebook(self, style="TNotebook")
        notebook.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        for yoga_name, info in YOGA_TYPES.items():
            tab = self.create_yoga_tab(info["image"], info["desc"], info["color"])
            notebook.add(tab, text=yoga_name)

    def create_yoga_tab(self, image_file, text, bg_color):
        frame = tk.Frame(bg=bg_color)

        try:
            img = Image.open(image_file)
            img = img.resize((400, 200), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            label = tk.Label(frame, image=photo, bg=bg_color)
            label.image = photo
            label.pack(pady=10)
        except Exception as e:
            print(f"Error loading image {image_file}: {e}")

        st = ScrolledText(frame, wrap=tk.WORD, font=("Tahoma", 18), bg="white", fg="black")
        st.insert(tk.END, text)
        st.config(state=tk.DISABLED)
        st.pack(expand=True, fill=tk.BOTH, padx=40, pady=20)
        return frame


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Types of Yoga")
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry(f"{w}x{h}+0+0")

    yoga_types = YogaTypesComponent(root)
    yoga_types.pack(expand=True, fill=tk.BOTH)

    root.mainloop()
