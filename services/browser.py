import subprocess

def open_with_profile(chrome_path, profile, url):
    subprocess.Popen([
        chrome_path,
        f"--profile-directory={profile}",
        url
    ])
