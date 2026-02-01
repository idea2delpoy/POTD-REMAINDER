import tkinter as tk
from ui.schedule_editor import ScheduleEditor
from ui.theme import *

class HomeScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG)

        tk.Label(
            self,
            text="POTD Scheduler",
            font=("Segoe UI", 22, "bold"),
            fg=TEXT,
            bg=BG
        ).pack(pady=25)

        self.create_card("LeetCode", "leetcode")
        self.create_card("GeeksforGeeks", "gfg")

    def create_card(self, title, platform):
        card = tk.Frame(self, bg=CARD, height=90, cursor="hand2")
        card.pack(fill="x", padx=80, pady=12)
        card.pack_propagate(False)

        title_lbl = tk.Label(
            card,
            text=title,
            font=("Segoe UI", 16, "bold"),
            fg=TEXT,
            bg=CARD,
            cursor="hand2"
        )
        title_lbl.pack(anchor="w", padx=20, pady=(15, 0))

        subtitle_lbl = tk.Label(
            card,
            text="Configure daily reminders",
            font=("Segoe UI", 10),
            fg=MUTED,
            bg=CARD,
            cursor="hand2"
        )
        subtitle_lbl.pack(anchor="w", padx=20)

        btn = tk.Button(
            card,
            text="Edit Schedule",
            bg=BUTTON,
            fg="white",
            relief="flat",
            command=lambda: self.open_editor(platform)
        )
        btn.pack(anchor="e", padx=20, pady=15)

        # 🔥 Make entire card clickable
        card.bind("<Button-1>", lambda e: self.open_editor(platform))
        title_lbl.bind("<Button-1>", lambda e: self.open_editor(platform))
        subtitle_lbl.bind("<Button-1>", lambda e: self.open_editor(platform))

    def open_editor(self, platform):
        self.master.current_frame.destroy()
        self.master.current_frame = ScheduleEditor(self.master, platform)
        self.master.current_frame.pack(fill="both", expand=True)
