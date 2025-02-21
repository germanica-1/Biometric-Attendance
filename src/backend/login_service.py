import mysql.connector
from dotenv import load_dotenv
import os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox
from src.frontend.admin_gui import admin_panel
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
        print("window created")
        
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
    """Handles the login process, including validation and database authentication."""
    global trial_no  # Track login attempts globally

    # Validate username and password inputs
    if not username.strip() or not password.strip():
        QMessageBox.critical(window, "Entry Error", "Please enter both username and password.")
        return

    try:
        # Connect to the database
        mydb = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            cursorclass=pymysql.cursors.DictCursor,  # Return results as dictionaries
        )
        mycursor = mydb.cursor()
        print("Connected to database")
    except pymysql.MySQLError as err:
        print(f"Database connection error: {err}")
        QMessageBox.critical(window, "Connection Error", "Failed to connect to the database.")
        return

    try:
        print("error3")
        # Execute the SQL query
        command = "SELECT * FROM login WHERE Username = %s AND Password = %s"
        mycursor.execute(command, (username, password))
        myresult = mycursor.fetchone()

        if myresult is None:
            # Invalid credentials
            QMessageBox.warning(window, "Invalid Credentials", "Incorrect UserID or Password.")
            trial(window)  # Increment failed attempts
            return
        else:
            # Successful login
            QMessageBox.information(window, "Login Successful", "Welcome!")
            print("Switching to admin panel...")

            # Hide login window and open admin panel
            print("error4")
            window.hide()

            if not hasattr(QtWidgets.QApplication.instance(), "admin_window") or QtWidgets.QApplication.instance().admin_window is None:
                window.admin_window = AdminPanelWindow(window)  # Pass parent reference to prevent garbage
                window.admin_window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            # Keep a reference to the Admin Panel to prevent it from closing
            window.admin_window.show()
            window.admin_window.activateWindow()
            
    except mysql.connector.Error as err:
        print(f"SQL query error: {err}")
        QMessageBox.critical(window, "Query Error", "An error occurred while checking credentials.")
    except Exception as e:
        print(f"Unexpected error: {e}")
        QMessageBox.critical(window, "Error", "An unexpected error occurred.")
    finally:
        # Close the database connection
        if mydb:
            mycursor.close()
            mydb.close()
            print("✅ Database connection closed")