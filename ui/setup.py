import tkinter as tk
from tkinter import filedialog, messagebox
from services.chrome_path import detect_chrome_path
from services.chrome_profiles import detect_chrome_profiles
from utils.file_utils import write_json
from utils.app_paths import get_storage_path

CONFIG_FILE = get_storage_path("user_config.json")


class SetupScreen(tk.Frame):
    def __init__(self, master, on_finish):
        super().__init__(master, bg="#0f172a")
        self.on_finish = on_finish
        self.chrome_path = None

        tk.Label(
            self,
            text="Initial Setup",
            font=("Segoe UI", 20, "bold"),
            fg="white",
            bg="#0f172a"
        ).pack(pady=20)

        self.status = tk.Label(
            self,
            text="Detecting Chrome...",
            fg="#94a3b8",
            bg="#0f172a"
        )
        self.status.pack(pady=10)

        self.setup()

    def setup(self):
        self.chrome_path = detect_chrome_path()

        if self.chrome_path:
            self.status.config(text="Chrome detected automatically ✅")
        else:
            self.status.config(text="Chrome not found. Please select chrome.exe")
            tk.Button(
                self,
                text="Select chrome.exe",
                command=self.select_chrome
            ).pack(pady=10)

        tk.Button(
            self,
            text="Finish Setup",
            command=self.finish_setup
        ).pack(pady=20)

    def select_chrome(self):
        path = filedialog.askopenfilename(
            title="Select chrome.exe",
            filetypes=[("Chrome", "chrome.exe")]
        )
        if path:
            self.chrome_path = path
            self.status.config(text="Chrome selected manually ✅")

    def finish_setup(self):
        if not self.chrome_path:
            messagebox.showerror("Error", "Please select chrome.exe")
            return

        profiles = detect_chrome_profiles()

        write_json(CONFIG_FILE, {
            "chrome_path": self.chrome_path,
            "profiles": profiles
        })

        # Force navigation
        self.destroy()
        self.on_finish()
