import os

COMMON_CHROME_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
]

def detect_chrome_path():
    for path in COMMON_CHROME_PATHS:
        if os.path.exists(path):
            return path
    return None
