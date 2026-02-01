import pystray
from PIL import Image, ImageDraw
import threading

def create_image():
    img = Image.new("RGB", (64, 64), "white")
    d = ImageDraw.Draw(img)
    d.rectangle((16, 16, 48, 48), fill="black")
    return img

def start_tray(app):
    def on_open(icon, item):
        app.after(0, app.deiconify)

    def on_exit(icon, item):
        icon.stop()
        app.after(0, app.destroy)

    icon = pystray.Icon(
        "POTD Scheduler",
        create_image(),
        menu=pystray.Menu(
            pystray.MenuItem("Open", on_open),
            pystray.MenuItem("Exit", on_exit)
        )
    )

    threading.Thread(target=icon.run, daemon=True).start()
