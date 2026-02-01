import os
import sys

def enable_autostart(app_name="POTD Scheduler"):
    startup = os.path.join(
        os.environ["APPDATA"],
        r"Microsoft\Windows\Start Menu\Programs\Startup"
    )

    shortcut = os.path.join(startup, f"{app_name}.bat")

    if not os.path.exists(shortcut):
        with open(shortcut, "w") as f:
            f.write(f'start "" "{sys.executable}" "{sys.argv[0]}"')
