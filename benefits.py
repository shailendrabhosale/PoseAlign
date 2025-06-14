import tkinter as tk
from PIL import Image, ImageTk

# Dictionary of yoga poses with benefits and image filenames.
yoga_poses = {
    "Downward Dog": {
        "benefits": ("Lengthens and decompresses the spine, strengthens arms and legs, "
                     "improves circulation, and helps reduce stress by calming the mind."),
        "image": "downward_dog.jpg"
    },
    "Child's Pose": {
        "benefits": ("Gently stretches the back, hips, and shoulders while promoting deep relaxation "
                     "and reducing stress and anxiety."),
        "image": "child_pose1.jpg"
    },
    "Warrior II": {
        "benefits": ("Strengthens the legs, opens the chest and shoulders, improves focus, and supports "
                     "good posture for energy and balance."),
        "image": "warrior_2.jpg"
    },
    "Tree Pose": {
        "benefits": ("Improves balance, concentration, and body awareness by strengthening the legs "
                     "and enhancing stability."),
        "image": "tree_pose.jpg"
    },
    "Restorative Yoga": {
        "benefits": ("Uses supported, long-held postures to promote deep relaxation, stress relief, and recovery, "
                     "making it ideal for healing and rejuvenation."),
        "image": "restorative_2.jpg"
    }
}

class YogaBenefitsComponent(tk.Frame):
    def __init__(self, parent, width, height, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.width = width
        self.height = height
        self.configure(bg="#ECEFF1")
        
        # Header Section
        self.header_frame = tk.Frame(self, bg="#AC90F6", height=100)
        self.header_frame.pack(fill=tk.X)
        title_label = tk.Label(self.header_frame,
                               text="Discover the Benefits of Yoga Poses",
                               font=("Tahoma", 24, "bold"),
                               bg="#AC90F6", fg="white")
        title_label.pack(pady=20)
        
        # Main Frame
        main_frame = tk.Frame(self, bg="#ECEFF1")
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        # Left Navigation Panel
        self.left_frame = tk.Frame(main_frame, width=250, bg="#ECEFF1")
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # Right Detail Panel
        self.right_frame = tk.Frame(main_frame, bg="white", bd=2, relief=tk.GROOVE)
        self.right_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
        
        # Create navigation buttons
        for pose in yoga_poses:
            btn = tk.Button(self.left_frame,
                            text=pose,
                            font=("Verdana", 13, "bold"),
                            command=lambda p=pose: self.display_pose(p),
                            bg="#AC90F6", fg="white", activebackground="#8E6CE0",
                            bd=0, padx=10, pady=8)
            btn.pack(pady=10, fill=tk.X, padx=20)
        
        self.display_pose("Downward Dog")
    
    def display_pose(self, pose_name):
        for widget in self.right_frame.winfo_children():
            widget.destroy()
            
        title = tk.Label(self.right_frame,
                         text=pose_name,
                         font=("Tahoma", 20, "bold"),
                         bg="white", fg="#333")
        title.pack(pady=20)
        
        image_file = yoga_poses[pose_name]["image"]
        try:
            img = Image.open(image_file)
            img = img.resize((450, 300), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
        except Exception as e:
            photo = None
        
        if photo:
            image_label = tk.Label(self.right_frame, image=photo, bg="white")
            image_label.image = photo
            image_label.pack(pady=10)
        
        benefits = yoga_poses[pose_name]["benefits"]
        text_label = tk.Label(self.right_frame,
                              text=benefits,
                              font=("Arial", 14),
                              bg="white", fg="#555",
                              wraplength=600,
                              justify=tk.LEFT)
        text_label.pack(pady=20, padx=30)

if __name__ == "__main__":
    root = tk.Tk()
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry("%dx%d+0+0" % (w, h))
    root.title("Yoga Pose Tips")
    
    yoga_component = YogaBenefitsComponent(root, w, h)
    yoga_component.pack(expand=True, fill=tk.BOTH)
    
    root.mainloop()
