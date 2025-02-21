import sys
import os
from PyQt5.QtWidgets import QApplication
from src.frontend.login_gui import LoginPanel  # Import LoginPanel instead of Ui_Form

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

def main():
    print("Starting Biometric Attendance System...")  # Now prints first
    app = QApplication(sys.argv)  # Create PyQt application instance
    window = LoginPanel()  # Create an instance of the Login GUI
    window.show()  # Show the login window
    sys.exit(app.exec_())  # Execute the application loop

if __name__ == "__main__":
    main()
