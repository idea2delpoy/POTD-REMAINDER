import tkinter as tk
from ui.theme import *

class TimePicker(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=CARD)

        self.hour = tk.Spinbox(
            self,
            from_=0,
            to=23,
            width=3,
            font=("Segoe UI", 11),
            bg=BG,
            fg=TEXT,
            buttonbackground=CARD,
            relief="flat",
            format="%02.0f"
        )

        self.minute = tk.Spinbox(
            self,
            from_=0,
            to=59,
            width=3,
            font=("Segoe UI", 11),
            bg=BG,
            fg=TEXT,
            buttonbackground=CARD,
            relief="flat",
            format="%02.0f"
        )

        self.hour.pack(side="left", padx=(15, 2), pady=5)
        tk.Label(self, text=":", bg=CARD, fg=TEXT,
                 font=("Segoe UI", 12, "bold")).pack(side="left")
        self.minute.pack(side="left", padx=(2, 15), pady=5)

        # Default time = current system time (nice UX)
        self.set_current_time()

    def set_current_time(self):
        from datetime import datetime
        now = datetime.now()
        self.hour.delete(0, "end")
        self.hour.insert(0, f"{now.hour:02d}")
        self.minute.delete(0, "end")
        self.minute.insert(0, f"{now.minute:02d}")

    def get_time(self):
        h = int(self.hour.get())
        m = int(self.minute.get())
        return f"{h:02d}:{m:02d}"
