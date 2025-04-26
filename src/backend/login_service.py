import sqlite3
import os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox
from src.frontend.admin_panel import admin_panel
from passlib.hash import pbkdf2_sha256
import sys

# Database path (adjust to your actual path)
DB_PATH = os.path.join("config", "mydb.sqlite")

# Global trial counter
trial_no = 0

class AdminPanelWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = admin_panel()
        self.setWindowTitle("Admin Panel")
        self.ui.setupUi(self)
        self.resize(900, 700)

def trial(window):
    """Handles failed login attempts and closes window after 3 attempts."""
    global trial_no
    trial_no += 1
    QMessageBox.warning(window, "Warning!", f"Attempted Login: {trial_no}/3")

    if trial_no == 3:
        print("Closing the login window after 3 failed attempts.")
        window.close()

def loginuser(username, password, window):
    """Handles the login process with SQLite database."""
    global trial_no

    # Input validation
    if not username.strip() or not password.strip():
        QMessageBox.critical(window, "Entry Error", "Please enter both username and password.")
        return

    conn = None
    try:
        # Connect to SQLite database
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  # Enable dictionary-style access
        cursor = conn.cursor()

        # Fetch user by username
        cursor.execute("SELECT * FROM login WHERE Username = ?", (username,))
        user = cursor.fetchone()

        if not user:
            QMessageBox.warning(window, "Invalid Credentials", "Username not found.")
            trial(window)
            return

        stored_hash = user['Password']
        
        # Password verification
        try:
            if pbkdf2_sha256.identify(stored_hash):
                valid = pbkdf2_sha256.verify(password, stored_hash)
            else:
                # Fallback for plaintext comparison (INSECURE - for migration only)
                valid = False
                if stored_hash == password:
                    QMessageBox.warning(window, "Security Warning", 
                                      "Your password is stored insecurely. Please contact admin.")
                    valid = True
                
            if not valid:
                QMessageBox.warning(window, "Invalid Credentials", "Incorrect password.")
                trial(window)
                return

        except ValueError as e:
            QMessageBox.critical(window, "Error", f"Password verification failed: {str(e)}")
            return

        # Successful login
        QMessageBox.information(window, "Login Successful", "Welcome!")
        window.hide()
        
        if not hasattr(QtWidgets.QApplication.instance(), "admin_window"):
            window.admin_window = AdminPanelWindow(window)
            window.admin_window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        window.admin_window.show()
        window.admin_window.activateWindow()

    except Exception as e:
        QMessageBox.critical(window, "Error", f"An error occurred: {str(e)}")
    finally:
        if conn:
            conn.close()

# Sample usage if running this module directly
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    # Test database connection
    try:
        conn = sqlite3.connect(DB_PATH)
        print("Successfully connected to SQLite database")
        conn.close()
    except Exception as e:
        print(f"Database connection failed: {str(e)}")
    
    sys.exit(app.exec_())