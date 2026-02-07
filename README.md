# 🕒 POTD Scheduler  
**Automate your daily coding practice. Never miss a LeetCode or GFG Problem of the Day again.**

---

## 📌 About the App
**POTD Scheduler** is a Windows productivity tool designed for developers who want to stay consistent with competitive programming. It automates the tedious task of manually navigating to LeetCode and GeeksforGeeks every day.

If your PC is on, the app **auto-opens** the problem in your preferred Chrome profile at your chosen time. If your system is offline, our backend sends an **email reminder** so you can catch up later.

---

## 🚀 Features
* **⏰ Smart Scheduling:** Set specific times for LeetCode and GFG problems to open.
* **🌐 Chrome Integration:** Supports profile selection so you're already logged in.
* **📬 Fail-Safe Notifications:** Email alerts via SendGrid if your system is offline during a schedule.
* **🖥️ Stealth Mode:** Runs quietly in the System Tray (background).
* **🔄 Cloud Sync:** Schedules are synced to a FastAPI backend for persistence.
* **🔐 Secure by Design:** No API keys or sensitive secrets are stored in the `.exe`.

---

## 🧱 Architecture (High-Level)



* **Desktop App:** Python (Tkinter + PyInstaller)
* **Backend:** FastAPI (Hosted on Render)
* **Database:** SQLite
* **Email Service:** SendGrid

---

## 🛠 Tech Stack
### **Desktop App**
* **Python / Tkinter:** UI and logic.
* **PyInstaller:** Bundling into a standalone EXE.
* **Inno Setup:** Professional Windows installer creation.
* **pystray:** System tray integration.

### **Backend**
* **FastAPI:** High-performance REST API.
* **Uvicorn:** ASGI server for production.
* **SendGrid:** Reliable email delivery.

---

## ⬇️ Download & Installation

### **For End Users**
1.  **Download:** [Setup-POTD-Scheduler.exe](https://www.mediafire.com/file/14jpfg2u4ytkrws/Setup-POTD-Scheduler.exe/file)
2.  **Install:** Run the installer and follow the wizard.
3.  **Setup:**
    * Select your Chrome path (usually auto-detected).
    * Choose your Chrome Profile/Account.
    * Set your preferred time and click **Save**.
4.  The app will minimize to the tray and work its magic!

---

## 👨‍💻 For Developers (Local Setup)

### **1. Clone the Repository**
```bash
git clone [https://github.com/idea2delpoy/POTD-REMAINDER.git](https://github.com/idea2delpoy/POTD-REMAINDER.git)
cd POTD-REMAINDER
2. Run Backend
Bash
cd backend
pip install -r requirements.txt
# Create a .env file with:
# SENDGRID_API_KEY=your_key
# SENDER_EMAIL=your_verified_email
python -m uvicorn main:app --reload
3. Run Desktop App
Bash
# In the root directory
pip install -r requirements.txt
python app.py
4. Build the Executable
Bash
python -m PyInstaller --onefile --noconsole --name "POTD-Scheduler" app.py
❌ Uninstallation
Standard: Control Panel → Programs → Uninstall → POTD Scheduler.

Clean Up: To remove local logs and configs, delete:

C:\Users\<YourName>\AppData\Local\POTD_Scheduler

⚠️ Known Limitations
OS: Windows only.

Browser: Requires Google Chrome.

Email: Check your Spam folder if notifications don't appear initially.

🗺 Future Roadmap
[ ] Support for macOS and Linux.

[ ] Auto-update mechanism.

[ ] Windows native toast notifications.

[ ] Integration with Codeforces.

🧑‍💻 Author
Built by [Idea2Deploy] A productivity tool for the developer community.


---

**Would you like me to generate a license file (MIT or Apache) to include in your repository as well?**
