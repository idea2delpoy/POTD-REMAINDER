import tkinter as tk
from utils.file_utils import read_json, write_json
from utils.app_paths import get_storage_path
from services.chrome_profiles import detect_chrome_profiles
from services.backend import sync
from ui.time_picker import TimePicker
from ui.theme import *

SCHEDULE_FILE = get_storage_path("schedules.json")


class ScheduleEditor(tk.Frame):
    def __init__(self, master, platform):
        super().__init__(master, bg=BG)
        self.platform = platform

        # 🔒 IMPORTANT: use grid at root level
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=1)

        # ---------- TITLE ----------
        title = tk.Label(
            self,
            text=f"{platform.upper()} Reminder",
            font=("Segoe UI", 20, "bold"),
            fg=TEXT,
            bg=BG
        )
        title.grid(row=0, column=0, pady=(15, 5), sticky="n")

        # ---------- SCROLLABLE AREA ----------
        container = tk.Frame(self, bg=BG)
        container.grid(row=0, column=0, sticky="nsew", pady=(60, 0))

        canvas = tk.Canvas(container, bg=BG, highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        content = tk.Frame(canvas, bg=BG)
        canvas.create_window((0, 0), window=content, anchor="nw")

        content.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # ---------- CARD ----------
        card = tk.Frame(content, bg=CARD)
        card.pack(padx=80, pady=20, fill="x")

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

        # ---------- FIXED BOTTOM ACTION BAR ----------
        bottom = tk.Frame(self, bg=CARD, height=70)
        bottom.grid(row=1, column=0, sticky="ew")
        bottom.grid_propagate(False)

        tk.Button(
            bottom,
            text="Save Configuration",
            bg=BUTTON,
            fg="white",
            font=("Segoe UI", 12, "bold"),
            relief="flat",
            command=self.save
        ).pack(pady=(10, 5), padx=120, fill="x")

        tk.Button(
            bottom,
            text="← Back",
            bg=CARD,
            fg=MUTED,
            relief="flat",
            command=self.back
        ).pack()

    # ---------- HELPERS ----------
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

    # ---------- ACTIONS ----------
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
