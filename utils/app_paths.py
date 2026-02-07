import os
import sys

def get_app_data_dir():
    base = os.getenv("LOCALAPPDATA")
    app_dir = os.path.join(base, "POTD_Scheduler")
    os.makedirs(app_dir, exist_ok=True)
    return app_dir

def get_storage_path(filename):
    return os.path.join(get_app_data_dir(), filename)
