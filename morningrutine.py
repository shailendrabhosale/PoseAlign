'''import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import time

class RoutineApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Morning Routine & Diet Tracker")
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{w}x{h}+0+0")
        self.configure(bg="seashell2")

        self.custom_routines = []
        self.custom_diets = []

        # Custom styling for notebook tabs
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

        self.notebook = ttk.Notebook(self, style="TNotebook")
        self.notebook.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        self.routine_page = TrackerPage(self, "Morning Routine", self.custom_routines, w)
        self.diet_page = TrackerPage(self, "Diet Plan", self.custom_diets, w)

        self.notebook.add(self.routine_page, text="🌅 Morning Routine")
        self.notebook.add(self.diet_page, text="🥗 Diet Plan")


class TrackerPage(tk.Frame):
    def __init__(self, parent, title, items_list, screen_width):
        super().__init__(parent)
        self.configure(bg="seashell2")
        self.title = title
        self.items_list = items_list
        self.screen_width = screen_width
        self.check_vars = []

        # Changed header background color to purple
        self.header_frame = tk.Frame(self, bg="#6A1B9A", height=80)  # Purple color
        self.header_frame.pack(fill=tk.X)

        self.greeting_label = tk.Label(
            self.header_frame,
            text=title,
            font=("Segoe UI", 20, "bold"),  # reduced font size
            bg="#6A1B9A", fg="white"  # Purple background with white text
        )
        self.greeting_label.pack(pady=(10,0))

        self.clock_label = tk.Label(
            self.header_frame,
            font=("Segoe UI", 14),  # reduced font size
            bg="#6A1B9A", fg="white"  # Purple background with white text
        )
        self.clock_label.pack(pady=(0,10))
        self.update_clock()

        # Scrollable frame setup
        self.canvas = tk.Canvas(self, bg="seashell2", highlightthickness=0)
        self.scroll_frame = tk.Frame(self.canvas, bg="seashell2")
        self.scroll_window = self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        self.canvas.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", self.resize_window)
        self.canvas.bind("<Enter>", self.bind_scroll)
        self.canvas.bind("<Leave>", self.unbind_scroll)

        # Progress and Add button
        self.progress_frame = tk.Frame(self, bg="seashell2")
        self.progress_frame.pack(fill=tk.X, padx=30, pady=(10,20))

        self.progress_label = tk.Label(
            self.progress_frame,
            text="Completion:",
            font=("Segoe UI", 14),
            bg="seashell2", fg="#2C3E50"
        )
        self.progress_label.pack(side=tk.LEFT, padx=(0,10))

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            variable=self.progress_var,
            maximum=100,
            length=400
        )
        self.progress_bar.pack(side=tk.LEFT)

        self.add_button = tk.Button(
            self.progress_frame,
            text=f"+ Add to {title}",
            command=self.add_item,
            font=("Segoe UI", 12, "bold"),
            bg="#AC90F6",
            fg="white",
            activebackground="#9B7FF6",
            activeforeground="white",
            bd=0,
            padx=20,
            pady=5
        )
        self.add_button.pack(side=tk.RIGHT, padx=10)

        self.refresh_items()

    def update_clock(self):
        current_time = time.strftime("%I:%M:%S %p")
        self.clock_label.config(text=current_time)
        self.after(1000, self.update_clock)

    def resize_window(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.scroll_window, width=canvas_width)

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def scroll_up(self, event):
        self.canvas.yview_scroll(-1, "units")

    def scroll_down(self, event):
        self.canvas.yview_scroll(1, "units")

    def refresh_items(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        self.check_vars.clear()

        card_width = int(self.screen_width * 0.7)
        card_height = 90

        for idx, item in enumerate(self.items_list):
            var = tk.BooleanVar()
            self.check_vars.append(var)

            wrapper = tk.Frame(self.scroll_frame, bg="seashell2")
            wrapper.pack(pady=10)

            card = tk.Frame(
                wrapper,
                bg="#D1C4E9",
                bd=2,
                relief=tk.RIDGE,
                width=card_width,
                height=card_height
            )
            card.pack()
            card.pack_propagate(False)

            chk = tk.Checkbutton(
                card,
                text=item,
                variable=var,
                font=("Segoe UI", 14),
                bg="#D1C4E9",
                fg="black",
                activebackground="#D1C4E9",
                wraplength=card_width - 40,
                justify=tk.LEFT,
                anchor="w",
                padx=10,
                command=self.update_progress
            )
            chk.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.update_progress()

    def update_progress(self):
        completed = sum(var.get() for var in self.check_vars)
        total = len(self.check_vars)
        percentage = (completed / total) * 100 if total > 0 else 0
        self.progress_var.set(percentage)

    def add_item(self):
        custom_popup = CustomInputPopup(self, f"Enter a new item for {self.title}:")
        self.wait_window(custom_popup)  # Wait for the popup to close before proceeding
        if custom_popup.result:
            item = custom_popup.result.strip()
            if item:
                self.items_list.append(item)
                self.refresh_items()
            else:
                CustomMessageBox(self, "Input Error", "Item cannot be empty.")


    def bind_scroll(self, event=None):
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        self.canvas.bind_all("<Up>", self.scroll_up)
        self.canvas.bind_all("<Down>", self.scroll_down)

    def unbind_scroll(self, event=None):
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Up>")
        self.canvas.unbind_all("<Down>")


class CustomInputPopup(tk.Toplevel):
    def __init__(self, parent, prompt):
        super().__init__(parent)
        self.title("Add Item")
        self.geometry("300x150")
        self.configure(bg="seashell2")
        self.result = None

        # Prompt Label
        prompt_label = tk.Label(self, text=prompt, font=("Segoe UI", 12), bg="seashell2", fg="black")
        prompt_label.pack(pady=(20, 10))

        # Entry Box
        self.entry = tk.Entry(self, font=("Segoe UI", 14), bg="white", fg="black", width=25)
        self.entry.pack(pady=(0, 20))
        self.entry.focus()

        # Submit Button
        submit_button = tk.Button(
            self,
            text="Add",
            command=self.on_submit,
            font=("Segoe UI", 12, "bold"),
            bg="#AC90F6",
            fg="white",
            activebackground="#9B7FF6",
            activeforeground="white",
            bd=0,
            padx=20,
            pady=5
        )
        submit_button.pack()

    def on_submit(self):
        self.result = self.entry.get()
        self.destroy()


class CustomMessageBox(tk.Toplevel):
    def __init__(self, parent, title, message):
        super().__init__(parent)
        self.title(title)
        self.geometry("300x150")
        self.configure(bg="seashell2")

        # Message Label
        message_label = tk.Label(self, text=message, font=("Segoe UI", 12), bg="seashell2", fg="black")
        message_label.pack(pady=(30, 10))

        # Ok Button
        ok_button = tk.Button(
            self,
            text="Ok",
            command=self.destroy,
            font=("Segoe UI", 12, "bold"),
            bg="#AC90F6",
            fg="white",
            activebackground="#9B7FF6",
            activeforeground="white",
            bd=0,
            padx=20,
            pady=5
        )
        ok_button.pack()


if __name__ == "__main__":
    app = RoutineApp()
    app.mainloop()
'''

import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import time

class RoutineApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Morning Routine & Diet Tracker")
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{w}x{h}+0+0")
        self.configure(bg="seashell2")

        self.custom_routines = []
        self.custom_diets = []

        # Custom styling for notebook tabs
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

        self.notebook = ttk.Notebook(self, style="TNotebook")
        self.notebook.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        self.routine_page = TrackerPage(self, "Morning Routine", self.custom_routines, w)
        self.diet_page = TrackerPage(self, "Diet Plan", self.custom_diets, w)

        self.notebook.add(self.routine_page, text="🌅 Morning Routine")
        self.notebook.add(self.diet_page, text="🥗 Diet Plan")


class TrackerPage(tk.Frame):
    def __init__(self, parent, title, items_list, screen_width):
        super().__init__(parent)
        self.configure(bg="seashell2")
        self.title = title
        self.items_list = items_list
        self.screen_width = screen_width
        self.check_vars = []

        self.header_frame = tk.Frame(self, bg="#6A1B9A", height=80)
        self.header_frame.pack(fill=tk.X)

        self.greeting_label = tk.Label(
            self.header_frame,
            text=title,
            font=("Segoe UI", 20, "bold"),
            bg="#6A1B9A", fg="white"
        )
        self.greeting_label.pack(pady=(10,0))

        self.clock_label = tk.Label(
            self.header_frame,
            font=("Segoe UI", 14),
            bg="#6A1B9A", fg="white"
        )
        self.clock_label.pack(pady=(0,10))
        self.update_clock()

        # Scrollable frame
        self.canvas = tk.Canvas(self, bg="seashell2", highlightthickness=0)
        self.scroll_frame = tk.Frame(self.canvas, bg="seashell2")
        self.scroll_window = self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        self.canvas.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", self.resize_window)
        self.canvas.bind("<Enter>", self.bind_scroll)
        self.canvas.bind("<Leave>", self.unbind_scroll)

        self.progress_frame = tk.Frame(self, bg="seashell2")
        self.progress_frame.pack(fill=tk.X, padx=30, pady=(10,20))

        self.progress_label = tk.Label(
            self.progress_frame,
            text="Completion:",
            font=("Segoe UI", 14),
            bg="seashell2", fg="#2C3E50"
        )
        self.progress_label.pack(side=tk.LEFT, padx=(0,10))

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            variable=self.progress_var,
            maximum=100,
            length=400
        )
        self.progress_bar.pack(side=tk.LEFT)

        self.add_button = tk.Button(
            self.progress_frame,
            text=f"+ Add to {title}",
            command=self.add_item,
            font=("Segoe UI", 12, "bold"),
            bg="#AC90F6",
            fg="white",
            activebackground="#9B7FF6",
            activeforeground="white",
            bd=0,
            padx=20,
            pady=5
        )
        self.add_button.pack(side=tk.RIGHT, padx=10)

        self.refresh_items()

    def update_clock(self):
        current_time = time.strftime("%I:%M:%S %p")
        self.clock_label.config(text=current_time)
        self.after(1000, self.update_clock)

    def resize_window(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.scroll_window, width=canvas_width)

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def scroll_up(self, event):
        self.canvas.yview_scroll(-1, "units")

    def scroll_down(self, event):
        self.canvas.yview_scroll(1, "units")

    def refresh_items(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        self.check_vars.clear()

        card_width = int(self.screen_width * 0.7)
        card_height = 90

        for idx, item in enumerate(self.items_list):
            var = tk.BooleanVar()
            self.check_vars.append(var)

            wrapper = tk.Frame(self.scroll_frame, bg="seashell2")
            wrapper.pack(pady=10)

            card = tk.Frame(
                wrapper,
                bg="#D1C4E9",
                bd=2,
                relief=tk.RIDGE,
                width=card_width,
                height=card_height
            )
            card.pack()
            card.pack_propagate(False)

            item_frame = tk.Frame(card, bg="#D1C4E9")
            item_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

            chk = tk.Checkbutton(
                item_frame,
                text=item,
                variable=var,
                font=("Segoe UI", 14),
                bg="#D1C4E9",
                fg="black",
                activebackground="#D1C4E9",
                wraplength=card_width - 100,
                justify=tk.LEFT,
                anchor="w",
                padx=10,
                command=self.update_progress
            )
            chk.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            delete_btn = tk.Button(
                item_frame,
                text="🗑 Delete",
                command=lambda i=idx: self.delete_item(i),
                font=("Segoe UI", 12),
                bg="#EF5350",
                fg="white",
                activebackground="#E53935",
                activeforeground="white",
                bd=0,
                padx=10,
                pady=5
            )
            delete_btn.pack(side=tk.RIGHT)

        self.update_progress()

    def update_progress(self):
        completed = sum(var.get() for var in self.check_vars)
        total = len(self.check_vars)
        percentage = (completed / total) * 100 if total > 0 else 0
        self.progress_var.set(percentage)

    def add_item(self):
        custom_popup = CustomInputPopup(self, f"Enter a new item for {self.title}:")
        self.wait_window(custom_popup)
        if custom_popup.result:
            item = custom_popup.result.strip()
            if item:
                self.items_list.append(item)
                self.refresh_items()
            else:
                CustomMessageBox(self, "Input Error", "Item cannot be empty.")

    def delete_item(self, index):
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete:\n\n'{self.items_list[index]}'?")
        if confirm:
            del self.items_list[index]
            self.refresh_items()

    def bind_scroll(self, event=None):
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        self.canvas.bind_all("<Up>", self.scroll_up)
        self.canvas.bind_all("<Down>", self.scroll_down)

    def unbind_scroll(self, event=None):
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Up>")
        self.canvas.unbind_all("<Down>")


class CustomInputPopup(tk.Toplevel):
    def __init__(self, parent, prompt):
        super().__init__(parent)
        self.title("Add Item")
        self.geometry("300x150")
        self.configure(bg="seashell2")
        self.result = None

        prompt_label = tk.Label(self, text=prompt, font=("Segoe UI", 12), bg="seashell2", fg="black")
        prompt_label.pack(pady=(20, 10))

        self.entry = tk.Entry(self, font=("Segoe UI", 14), bg="white", fg="black", width=25)
        self.entry.pack(pady=(0, 20))
        self.entry.focus()

        submit_button = tk.Button(
            self,
            text="Add",
            command=self.on_submit,
            font=("Segoe UI", 12, "bold"),
            bg="#AC90F6",
            fg="white",
            activebackground="#9B7FF6",
            activeforeground="white",
            bd=0,
            padx=20,
            pady=5
        )
        submit_button.pack()

    def on_submit(self):
        self.result = self.entry.get()
        self.destroy()


class CustomMessageBox(tk.Toplevel):
    def __init__(self, parent, title, message):
        super().__init__(parent)
        self.title(title)
        self.geometry("300x150")
        self.configure(bg="seashell2")

        message_label = tk.Label(self, text=message, font=("Segoe UI", 12), bg="seashell2", fg="black")
        message_label.pack(pady=(30, 10))

        ok_button = tk.Button(
            self,
            text="Ok",
            command=self.destroy,
            font=("Segoe UI", 12, "bold"),
            bg="#AC90F6",
            fg="white",
            activebackground="#9B7FF6",
            activeforeground="white",
            bd=0,
            padx=20,
            pady=5
        )
        ok_button.pack()


if __name__ == "__main__":
    app = RoutineApp()
    app.mainloop()































