import time
import threading
from datetime import datetime
from utils.file_utils import read_json, write_json
from utils.app_paths import get_storage_path
from services.leetcode_potd import get_leetcode_potd
from services.gfg_potd import get_gfg_potd
from services.browser import open_with_profile
from services.backend import sync

CONFIG_FILE = get_storage_path("user_config.json")
SCHEDULE_FILE = get_storage_path("schedules.json")

# 🔒 GLOBAL FLAG
_scheduler_started = False


def scheduler_loop():
    while True:
        config = read_json(CONFIG_FILE)
        schedules = read_json(SCHEDULE_FILE, [])

        if not config or not schedules:
            time.sleep(30)
            continue

        chrome_path = config.get("chrome_path")
        now = datetime.now().strftime("%H:%M")
        today = datetime.now().strftime("%Y-%m-%d")

        for task in schedules:
            if not task.get("enabled"):
                continue
            if task.get("time") != now:
                continue
            if task.get("last_executed") == today:
                continue

            try:
                if task["platform"] == "leetcode":
                    url = get_leetcode_potd()["url"]
                else:
                    url = get_gfg_potd()["url"]

                open_with_profile(chrome_path, task["profile"], url)

                task["last_executed"] = today
                if task["repeat"] == "once":
                    task["enabled"] = False

                sync(task["email"], schedules)

            except Exception:
                pass

        write_json(SCHEDULE_FILE, schedules)
        time.sleep(30)


def start_scheduler():
    global _scheduler_started

    # ✅ PREVENT MULTIPLE STARTS
    if _scheduler_started:
        return

    _scheduler_started = True

    thread = threading.Thread(
        target=scheduler_loop,
        daemon=True,
        name="POTD-Scheduler-Thread"
    )
    thread.start()
