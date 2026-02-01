import os
import json
import getpass

def _read_preferences(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None

def detect_chrome_profiles():
    user = getpass.getuser()
    chrome_base = rf"C:\Users\{user}\AppData\Local\Google\Chrome\User Data"

    email_profile_map = {}

    if not os.path.exists(chrome_base):
        return {}

    for folder in os.listdir(chrome_base):
        if folder == "Default" or folder.startswith("Profile"):
            pref_path = os.path.join(chrome_base, folder, "Preferences")
            if not os.path.exists(pref_path):
                continue

            data = _read_preferences(pref_path)
            if not data:
                continue

            account_info = data.get("account_info")

            if isinstance(account_info, list):
                for acc in account_info:
                    email = acc.get("email")
                    if email:
                        email_profile_map[email] = folder

            elif isinstance(account_info, dict):
                email = account_info.get("email")
                if email:
                    email_profile_map[email] = folder

    return email_profile_map
