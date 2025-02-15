import sys
import os
from src.script.frontend import login_gui  # Import GUI but DON'T start it yet

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))


def main():
    print("Starting Biometric Attendance System...")  # Now prints first
    login_gui.window.mainloop()  # Start the GUI after printing


if __name__ == "__main__":
    main()
