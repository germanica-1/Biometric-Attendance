import mysql.connector
from dotenv import load_dotenv
import os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox
from src.frontend.admin_panel import admin_panel
import pymysql
import sys


# Load database environment variables
dotenv_path = os.path.join(
    "C:/Users/Krypton/Desktop/projects/Biometric Attendance/config/.env"
)
load_dotenv(dotenv_path=dotenv_path)


# Global trial counter
trial_no = 0
class AdminPanelWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)  # Pass parent reference to prevent garbage collection
        self.ui = admin_panel()  # Create an instance of admin_panel
        self.setWindowTitle("Admin Panel")
        self.ui.setupUi(self)  # Pass self (QMainWindow) to setup the UI correctly
        self.resize(900, 700)
        
# Function to handle login attempts
def trial(window):
    """Handles failed login attempts and closes window after 3 attempts."""
    global trial_no
    trial_no += 1
    QMessageBox.warning(window, "Warning!", f"Attempted Login: {trial_no}/3")

    if trial_no ==3:
        print("Closing the login window after 3 failed attempts.")  # Debug message
        print("error1")
        window.close()
        
def loginuser(username, password, window):
    """Handles the login process with improved password verification."""
    global trial_no

    # Input validation
    if not username.strip() or not password.strip():
        QMessageBox.critical(window, "Entry Error", "Please enter both username and password.")
        return

    try:
        # Database connection
        mydb = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            cursorclass=pymysql.cursors.DictCursor,
        )
        mycursor = mydb.cursor()

        # Fetch user by username
        mycursor.execute("SELECT * FROM login WHERE Username = %s", (username,))
        myresult = mycursor.fetchone()

        if not myresult:
            QMessageBox.warning(window, "Invalid Credentials", "Username not found.")
            trial(window)
            return

        stored_hash = myresult['Password']
        
        # Flexible password verification
        from passlib.hash import pbkdf2_sha256
        try:
            if pbkdf2_sha256.identify(stored_hash):  # Check if it's a PBKDF2 hash
                valid = pbkdf2_sha256.verify(password, stored_hash)
            else:
                # Fallback for legacy hashes (like bcrypt or plaintext - INSECURE, migrate ASAP)
                valid = False
                if stored_hash == password:  # Plain text comparison (INSECURE)
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
        if mydb:
            mycursor.close()
            mydb.close()

