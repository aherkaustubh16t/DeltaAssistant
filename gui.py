# gui.py
import tkinter as tk
from PIL import Image, ImageTk
import time
import threading
import os

class FloatingGUI:
    def __init__(self, logo_path="data/logo.png"):
        self.root = tk.Tk()
        self.root.overrideredirect(True)  # remove title bar
        self.root.attributes("-topmost", True)
        self.root.geometry("+50+50")
        self.root.configure(bg="#222222")
        # allow transparency on Windows if desired: self.root.wm_attributes("-transparentcolor", "white")

        # Make draggable
        self.offset_x = 0
        self.offset_y = 0
        self.root.bind("<Button-1>", self.start_move)
        self.root.bind("<B1-Motion>", self.do_move)

        # Contents
        frame = tk.Frame(self.root, bg="#222222", padx=10, pady=6)
        frame.pack()

        # Logo
        if os.path.exists(logo_path):
            img = Image.open(logo_path).resize((64,64))
            self.logo_img = ImageTk.PhotoImage(img)
            self.logo_label = tk.Label(frame, image=self.logo_img, bg="#222222")
            self.logo_label.pack()
        else:
            self.logo_label = tk.Label(frame, text="JARVIS", fg="white", bg="#222222", font=("Segoe UI", 14))
            self.logo_label.pack()

        # Status
        self.status_var = tk.StringVar(value="Idle")
        self.status_label = tk.Label(frame, textvariable=self.status_var, fg="white", bg="#222222", font=("Segoe UI", 10))
        self.status_label.pack()

        # Time
        self.time_var = tk.StringVar()
        self.time_label = tk.Label(frame, textvariable=self.time_var, fg="white", bg="#222222", font=("Segoe UI", 9))
        self.time_label.pack()

        # Close button (small)
        close_btn = tk.Button(frame, text="✕", command=self.root.destroy, bg="#444", fg="white", bd=0)
        close_btn.place(relx=1.0, x=-6, y=6, anchor="ne")

        # Start clock update
        threading.Thread(target=self._update_time_loop, daemon=True).start()

    def start_move(self, event):
        self.offset_x = event.x_root - self.root.winfo_x()
        self.offset_y = event.y_root - self.root.winfo_y()

    def do_move(self, event):
        x = event.x_root - self.offset_x
        y = event.y_root - self.offset_y
        self.root.geometry(f"+{x}+{y}")

    def set_status(self, text):
        self.status_var.set(text)
        self.root.update_idletasks()

    def _update_time_loop(self):
        while True:
            ts = time.strftime("%a %d %b %Y  %I:%M:%S %p")
            self.time_var.set(ts)
            time.sleep(1)

    def run(self):
        self.root.mainloop()
