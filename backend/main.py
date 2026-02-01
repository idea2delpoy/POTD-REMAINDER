from fastapi import FastAPI
from datetime import datetime
import threading
import time

from reminder import send_missed_potd_email

app = FastAPI()

# In-memory store (later replace with DB)
# {
#   email: {
#       "schedules": [...],
#       "last_seen": datetime
#   }
# }
USER_DATA = {}


@app.post("/sync/schedules")
def sync_schedules(payload: dict):
    email = payload.get("email")
    schedules = payload.get("schedules")

    USER_DATA[email] = {
        "schedules": schedules,
        "last_seen": datetime.utcnow()
    }

    return {"status": "ok"}


def check_missed_schedules():
    """
    Runs continuously in background.
    Sends email if:
    - scheduled time passed
    - task not executed today
    - app was not running at scheduled time
    """
    while True:
        now = datetime.now()
        today = now.strftime("%Y-%m-%d")

        for email, data in USER_DATA.items():
            schedules = data["schedules"]
            last_seen = data["last_seen"]

            for task in schedules:
                if not task.get("enabled"):
                    continue

                try:
                    scheduled_time = datetime.strptime(
                        f"{today} {task['time']}",
                        "%Y-%m-%d %H:%M"
                    )
                except Exception:
                    continue

                # ❌ App/System OFF at scheduled time → send email
                if (
                    now > scheduled_time
                    and task.get("last_executed") != today
                    and last_seen < scheduled_time
                ):
                    send_missed_potd_email(
                        email=email,
                        platform=task["platform"],
                        scheduled_time=task["time"],
                        problem_url=get_problem_url(task["platform"])
                    )

                    # Mark as handled to avoid duplicate emails
                    task["last_executed"] = today

        time.sleep(120)  # check every 2 minutes


def get_problem_url(platform):
    """
    Fallback URL (later replace with exact POTD link)
    """
    if platform == "leetcode":
        return "https://leetcode.com/problemset/all/"
    elif platform == "gfg":
        return "https://practice.geeksforgeeks.org/problem-of-the-day"
    return ""


@app.on_event("startup")
def start_background_checker():
    threading.Thread(
        target=check_missed_schedules,
        daemon=True
    ).start()
