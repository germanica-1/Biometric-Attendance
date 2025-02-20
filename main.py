import sys
import os
from src.frontend.login_gui import LoginGUI  # Import the class
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))


def main():
    print("Starting Biometric Attendance System...")  # Now prints first
    app = LoginGUI()  # Create an instance of the Login GUI
    app.run()  # Start the GUI


if __name__ == "__main__":
    main()
