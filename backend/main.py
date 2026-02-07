from fastapi import FastAPI
from datetime import datetime
import threading
import time
import pytz

from db import SessionLocal, init_db, User, Schedule
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

    db = SessionLocal()

    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            user = User(email=email)
            db.add(user)
            db.commit()
            db.refresh(user)

        # Update last_seen
        user.last_seen = datetime.utcnow()

        # Replace schedules
        db.query(Schedule).filter(Schedule.user_id == user.id).delete()

        for s in schedules:
            db.add(Schedule(
                user_id=user.id,
                platform=s.get("platform"),
                time=s.get("time"),
                repeat=s.get("repeat"),
                enabled=s.get("enabled", True),
                last_executed=s.get("last_executed")
            ))

        db.commit()
        return {"status": "ok"}

    finally:
        db.close()


def get_problem_url(platform):
    if platform == "leetcode":
        return "https://leetcode.com/problemset/all/"
    elif platform == "gfg":
        return "https://practice.geeksforgeeks.org/problem-of-the-day"
    return ""


def check_missed_schedules():
    while True:
        db = SessionLocal()
        try:
            now_ist = datetime.now(IST)
            today = now_ist.strftime("%Y-%m-%d")

            users = db.query(User).all()

            for user in users:
                last_seen_utc = user.last_seen
                if not last_seen_utc:
                    continue

                last_seen_ist = last_seen_utc.replace(tzinfo=pytz.utc).astimezone(IST)

                for task in user.schedules:
                    if not task.enabled:
                        continue

                    try:
                        scheduled_time_ist = IST.localize(
                            datetime.strptime(f"{today} {task.time}", "%Y-%m-%d %H:%M")
                        )
                    except Exception:
                        continue

                    if (
                        now_ist > scheduled_time_ist
                        and task.last_executed != today
                        and last_seen_ist < scheduled_time_ist
                    ):
                        send_missed_potd_email(
                            email=user.email,
                            platform=task.platform,
                            scheduled_time=task.time,
                            problem_url=get_problem_url(task.platform)
                        )

                        task.last_executed = today
                        if task.repeat == "once":
                            task.enabled = False

            db.commit()

        finally:
            db.close()

        time.sleep(60)
