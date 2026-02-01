import time
import threading
from datetime import datetime
from utils.file_utils import read_json, write_json
from services.leetcode_potd import get_leetcode_potd
from services.gfg_potd import get_gfg_potd
from services.browser import open_with_profile
from services.backend import sync

SCHEDULE_FILE = "storage/schedules.json"
CONFIG_FILE = "storage/user_config.json"


def scheduler_loop():
    while True:
        schedules = read_json(SCHEDULE_FILE, [])
        config = read_json(CONFIG_FILE, {})

        chrome_path = config.get("chrome_path")
        if not chrome_path:
            time.sleep(30)
            continue

        now = datetime.now().strftime("%H:%M")
        today = datetime.now().strftime("%Y-%m-%d")

        for task in schedules:
            if not task["enabled"]:
                continue

            if task["time"] != now:
                continue

            if task["last_executed"] == today:
                continue

            try:
                if task["platform"] == "leetcode":
                    url = get_leetcode_potd()["url"]
                else:
                    url = get_gfg_potd()["url"]

                open_with_profile(
                    chrome_path,
                    task["profile"],
                    url
                )

                task["last_executed"] = today

                if task["repeat"] == "once":
                    task["enabled"] = False

                # Sync execution to backend
                sync(task["email"], schedules)

            except Exception:
                pass

        write_json(SCHEDULE_FILE, schedules)
        time.sleep(30)


def start_scheduler():
    thread = threading.Thread(target=scheduler_loop, daemon=True)
    thread.start()
