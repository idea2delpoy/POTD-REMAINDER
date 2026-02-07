from fastapi import FastAPI
from datetime import datetime
import threading
import time
import pytz

from db import init_db, get_conn
from reminder import send_missed_potd_email

app = FastAPI()
IST = pytz.timezone("Asia/Kolkata")


@app.on_event("startup")
def startup():
    init_db()
    threading.Thread(
        target=check_missed_schedules,
        daemon=True,
        name="Missed-Schedule-Checker"
    ).start()


@app.post("/sync/schedules")
def sync_schedules(payload: dict):
    email = payload.get("email")
    schedules = payload.get("schedules", [])

    if not email:
        return {"status": "error", "message": "email required"}

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO users (email, last_seen)
    VALUES (?, ?)
    ON CONFLICT(email) DO UPDATE SET last_seen=excluded.last_seen
    """, (email, datetime.utcnow().isoformat()))

    cur.execute("DELETE FROM schedules WHERE user_email=?", (email,))

    for s in schedules:
        cur.execute("""
        INSERT INTO schedules (user_email, platform, time, repeat, enabled, last_executed)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            email,
            s.get("platform"),
            s.get("time"),
            s.get("repeat"),
            1 if s.get("enabled", True) else 0,
            s.get("last_executed")
        ))

    conn.commit()
    conn.close()

    return {"status": "ok"}


def get_problem_url(platform):
    if platform == "leetcode":
        return "https://leetcode.com/problemset/all/"
    if platform == "gfg":
        return "https://practice.geeksforgeeks.org/problem-of-the-day"
    return ""


def check_missed_schedules():
    while True:
        try:
            conn = get_conn()
            cur = conn.cursor()

            now_ist = datetime.now(IST)
            today = now_ist.strftime("%Y-%m-%d")

            users = cur.execute("SELECT email, last_seen FROM users").fetchall()

            for u in users:
                email = u["email"]
                last_seen_utc = u["last_seen"]

                if not last_seen_utc:
                    continue

                last_seen_ist = datetime.fromisoformat(last_seen_utc).replace(
                    tzinfo=pytz.utc
                ).astimezone(IST)

                schedules = cur.execute(
                    "SELECT * FROM schedules WHERE user_email=? AND enabled=1",
                    (email,)
                ).fetchall()

                for task in schedules:
                    try:
                        scheduled_time_ist = IST.localize(
                            datetime.strptime(f"{today} {task['time']}", "%Y-%m-%d %H:%M")
                        )
                    except:
                        continue

                    if (
                        now_ist > scheduled_time_ist
                        and task["last_executed"] != today
                        and last_seen_ist < scheduled_time_ist
                    ):
                        send_missed_potd_email(
                            email=email,
                            platform=task["platform"],
                            scheduled_time=task["time"],
                            problem_url=get_problem_url(task["platform"])
                        )

                        cur.execute(
                            "UPDATE schedules SET last_executed=? WHERE id=?",
                            (today, task["id"])
                        )

                        if task["repeat"] == "once":
                            cur.execute("UPDATE schedules SET enabled=0 WHERE id=?", (task["id"],))

            conn.commit()
            conn.close()
        except Exception as e:
            print("Scheduler error:", e)

        time.sleep(60)
