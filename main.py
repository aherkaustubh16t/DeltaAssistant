# main.py
from gui import FloatingGUI
from listener import Assistant
import threading
import time

def main():
    gui = FloatingGUI(logo_path="data/logo.png")
    assistant = Assistant(gui)

    # start listener loop in background
    assistant.start_listening_loop()

    # run GUI (blocking)
    gui.run()

if __name__ == "__main__":
    main()
