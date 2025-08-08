# commands.py
import webbrowser
import os
import platform
import subprocess

PORTFOLIO_URL = "https://your-portfolio-link.example"  # change to your portfolio

def open_google():
    webbrowser.open("https://www.google.com")

def open_youtube():
    webbrowser.open("https://www.youtube.com")

def open_portfolio():
    webbrowser.open(PORTFOLIO_URL)

def open_app_windows(path):
    # Windows only helper: path is full exe path
    if platform.system() == "Windows":
        subprocess.Popen([path])
    else:
        raise NotImplementedError

def shutdown_system():
    if platform.system() == "Windows":
        os.system("shutdown /s /t 1")
    else:
        os.system("sudo shutdown -h now")

COMMAND_MAP = {
    "open google": open_google,
    "open youtube": open_youtube,
    "open portfolio": open_portfolio,
    # add more phrase mappings
}
