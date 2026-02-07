import requests

API = "https://potd-remainder.onrender.com"  # change after deployment

def sync(email, schedules):
    try:
        requests.post(
            f"{API}/sync/schedules",
            json={
                "email": email,
                "schedules": schedules
            },
            timeout=5
        )
    except requests.RequestException:
        # silently fail (offline, backend down)
        pass
