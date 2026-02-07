import tkinter as tk
from utils.file_utils import read_json
from utils.app_paths import get_storage_path
from services.scheduler import start_scheduler
from services.tray import start_tray
from ui.home import HomeScreen
from ui.setup import SetupScreen

CONFIG_FILE = get_storage_path("user_config.json")


class POTDSchedulerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("POTD Scheduler")
        self.geometry("600x500")
        self.resizable(False, False)

        self.current_frame = None

        # Start scheduler
        start_scheduler()

        # Tray behavior
        self.protocol("WM_DELETE_WINDOW", self.hide_to_tray)
        start_tray(self)

        # Decide initial screen
        if read_json(CONFIG_FILE):
            self.show_home()
        else:
            self.show_setup()

    def hide_to_tray(self):
        self.withdraw()

    def show_setup(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = SetupScreen(
            self,
            on_finish=self.show_home
        )
        self.current_frame.pack(fill="both", expand=True)

    def show_home(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = HomeScreen(self)
        self.current_frame.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = POTDSchedulerApp()
    app.mainloop()
