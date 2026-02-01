import tkinter as tk
from ui.theme import *
from utils.file_utils import read_json, write_json
from services.chrome_profiles import detect_chrome_profiles
from services.backend import sync
from ui.time_picker import TimePicker

SCHEDULE_FILE = "storage/schedules.json"


class ScheduleEditor(tk.Frame):
    def __init__(self, master, platform):
        super().__init__(master, bg=BG)
        self.platform = platform

        # ---- Title ----
        tk.Label(
            self,
            text=f"{platform.upper()} Reminder",
            font=("Segoe UI", 20, "bold"),
            fg=TEXT,
            bg=BG
        ).pack(pady=(20, 10))

        # ---- Scrollable Area ----
        canvas = tk.Canvas(self, bg=BG, highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        content = tk.Frame(canvas, bg=BG)
        canvas.create_window((0, 0), window=content, anchor="nw")

        content.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # ---- Card ----
        card = tk.Frame(content, bg=CARD)
        card.pack(padx=80, pady=10, fill="x")

        self.section(card, "Time")
        self.time_picker = TimePicker(card)
        self.time_picker.pack(pady=8)

        self.section(card, "Repeat")
        self.repeat_var = tk.StringVar(value="daily")
        self.radio(card, "Daily", "daily")
        self.radio(card, "One Time", "once")

        self.section(card, "Account")
        self.profiles = detect_chrome_profiles()
        self.email_var = tk.StringVar()

        if self.profiles:
            self.email_var.set(list(self.profiles.keys())[0])
            tk.OptionMenu(card, self.email_var, *self.profiles.keys()).pack(pady=8)
        else:
            tk.Label(card, text="No Chrome profiles found", fg="red", bg=CARD).pack()

        # ---- Buttons (ALWAYS VISIBLE) ----
        btn_frame = tk.Frame(self, bg=BG)
        btn_frame.pack(pady=15)

        tk.Button(
            btn_frame,
            text="Save Schedule",
            bg=BUTTON,
            fg="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            width=18,
            command=self.save
        ).pack(pady=(0, 8))

        tk.Button(
            btn_frame,
            text="← Back",
            bg=BG,
            fg=MUTED,
            relief="flat",
            command=self.back
        ).pack()

    def section(self, parent, text):
        tk.Label(
            parent,
            text=text,
            fg=MUTED,
            bg=CARD,
            font=("Segoe UI", 10)
        ).pack(anchor="w", padx=15, pady=(15, 2))

    def radio(self, parent, text, value):
        tk.Radiobutton(
            parent,
            text=text,
            variable=self.repeat_var,
            value=value,
            bg=CARD,
            fg=TEXT,
            selectcolor=CARD,
            activebackground=CARD
        ).pack(anchor="w", padx=20)

    def save(self):
        schedules = read_json(SCHEDULE_FILE, [])
        schedules = [s for s in schedules if s["platform"] != self.platform]

        email = self.email_var.get()

        schedules.append({
            "platform": self.platform,
            "time": self.time_picker.get_time(),
            "repeat": self.repeat_var.get(),
            "email": email,
            "profile": self.profiles.get(email),
            "enabled": True,
            "last_executed": None
        })

        write_json(SCHEDULE_FILE, schedules)
        sync(email, schedules)
        self.back()

    def back(self):
        self.master.show_home()
