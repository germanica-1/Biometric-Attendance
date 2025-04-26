import os
import pymysql
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
import requests
import sqlite3
import time
from dotenv import load_dotenv

#Refreshing and loading table database
def load_data(EmployeeTable):
    """Fetch employee data from SQLite database."""
    DB_PATH = os.path.join("config", "mydb.sqlite")
    
    conn = None
    try:
        # Connect to SQLite database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Set table columns
        EmployeeTable.setColumnCount(2)
        EmployeeTable.setHorizontalHeaderLabels(["ID", "Name"])
        
        # Fetch data
        cursor.execute("SELECT ID, Name FROM employee ORDER BY ID")
        results = cursor.fetchall()
        
        return results
        
    except sqlite3.Error as err:
        print(f"Database error: {err}")
        QMessageBox.critical(
            None, 
            "Database Error", 
            f"Failed to fetch data: {str(err)}"
        )
        return None
        
    except Exception as e:
        print(f"Unexpected error: {e}")
        QMessageBox.critical(
            None, 
            "Error", 
            f"An unexpected error occurred: {str(e)}"
        )
        return None
        
    finally:
        if conn:
            conn.close()


def delete_fingerprint(fingerprint_id, max_retries=3):
    """Send command to ESP8266 to delete fingerprint template with robust error handling"""
    env_path = os.path.join("config", ".env")
    load_dotenv(env_path)
    ap_ip = os.getenv("AP_WIFI")
    
    if not ap_ip:
        return False, "AP_WIFI environment variable not set"
    
    endpoint = "/delete_fingerprint"
    url = f"http://{ap_ip}{endpoint}"
    
    for attempt in range(max_retries):
        try:
            
            response = requests.post(
                url,
                json={"id": int(fingerprint_id)},
                timeout=10  # More reasonable timeout for local network
            )
            
            print(f"Delete response: {response.status_code} - {response.text}")
            
            if response.status_code == 200:
                # Check for different possible success responses
                if ("success" in response.text.lower() or 
                    "deleted" in response.text.lower()):
                    return True, "Fingerprint deleted successfully"
                return False, f"Unexpected response: {response.text}"
            
            return False, f"Device error (HTTP {response.status_code}): {response.text}"
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Connection error (attempt {attempt + 1}): {str(e)}"
            print(error_msg)
            if attempt == max_retries - 1:  # Last attempt
                return False, error_msg
            time.sleep(2)  # Wait before retrying
    
    return False, "Max retries exceeded"

def remove_employee(Name, load_data_callback=None):
    """Function to remove an employee by Name and their fingerprint using SQLite."""
    DB_PATH = os.path.join("config", "mydb.sqlite")
    Name = Name.strip()

    if not Name:
        QMessageBox.warning(None, "Input Error", "Please enter a Name to remove.")
        return

    conn = None
    try:
        # Connect to SQLite database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Check if Name exists and get ID
        cursor.execute("SELECT * FROM employee WHERE Name = ?", (Name,))
        user = cursor.fetchone()
        
        if not user:
            QMessageBox.warning(None, "Not Found", f"No employee found with Name: {Name}")
            return

        # Confirm deletion
        confirm = QMessageBox.question(
            None, "Confirm Deletion", 
            f"Are you sure you want to remove '{Name}' and their fingerprint?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            # Delete fingerprint first
            fingerprint_id = user[0]  # Access ID by index (first column)
            success, message = delete_fingerprint(fingerprint_id)
            
            if not success:
                response = QMessageBox.warning(
                    None, "Warning", 
                    f"Employee found but fingerprint deletion failed: {message}\n"
                    "Do you want to remove from database anyway?",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No
                )
                if response == QMessageBox.No:
                    return

            # Delete the user
            cursor.execute("DELETE FROM employee WHERE Name = ?", (Name,))
            conn.commit()
            QMessageBox.information(
                None, "Success", 
                f"Employee '{Name}' and fingerprint removed successfully."
            )
            
            if load_data_callback:
                load_data_callback()
        
    except sqlite3.Error as err:
        QMessageBox.critical(None, "Database Error", f"SQLite error: {str(err)}")
        if conn:
            conn.rollback()
    except Exception as e:
        QMessageBox.critical(None, "Error", f"Unexpected error: {str(e)}")
    finally:
        if conn:
            conn.close()