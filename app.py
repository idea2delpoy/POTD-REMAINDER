import tkinter as tk
from utils.file_utils import read_json
from services.scheduler import start_scheduler
from services.tray import start_tray
from ui.home import HomeScreen
from ui.setup import SetupScreen
from services.backend import sync

CONFIG_FILE = "storage/user_config.json"
SCHEDULE_FILE = "storage/schedules.json"


class POTDSchedulerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("POTD Scheduler")
        self.geometry("600x400")
        self.resizable(False, False)

        self.current_frame = None

        # Start background scheduler
        start_scheduler()

        # Sync schedules on startup
        schedules = read_json(SCHEDULE_FILE, [])
        if schedules:
            sync(schedules[0]["email"], schedules)

        # Tray behavior
        self.protocol("WM_DELETE_WINDOW", self.hide_to_tray)
        start_tray(self)

        # First-run setup or home
        if not read_json(CONFIG_FILE):
            self.show_setup()
        else:
            self.show_home()

    def hide_to_tray(self):
        self.withdraw()

    def show_setup(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = SetupScreen(self)
        self.current_frame.pack(fill="both", expand=True)

    def show_home(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = HomeScreen(self)
        self.current_frame.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = POTDSchedulerApp()
    app.mainloop()
