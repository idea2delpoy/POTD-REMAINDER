import tkinter as tk
from tkinter import filedialog
from services.chrome_path import detect_chrome_path
from services.chrome_profiles import detect_chrome_profiles
from utils.file_utils import write_json

CONFIG_FILE = "storage/user_config.json"

class SetupScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        tk.Label(self, text="Initial Setup",
                 font=("Segoe UI", 16, "bold")).pack(pady=20)

        self.chrome_path = detect_chrome_path()

        if not self.chrome_path:
            tk.Button(self, text="Select Chrome.exe",
                      command=self.select_chrome).pack(pady=10)
        else:
            tk.Label(self, text="Chrome detected ✔").pack()

        self.profiles = detect_chrome_profiles()
        tk.Label(self, text=f"Found {len(self.profiles)} Gmail account(s)").pack(pady=10)

        tk.Button(self, text="Finish Setup", command=self.finish).pack(pady=20)

    def select_chrome(self):
        self.chrome_path = filedialog.askopenfilename(
            title="Select chrome.exe",
            filetypes=[("Chrome", "chrome.exe")]
        )

    def finish(self):
        write_json(CONFIG_FILE, {
            "chrome_path": self.chrome_path,
            "profiles": self.profiles
        })
        self.master.show_home()
