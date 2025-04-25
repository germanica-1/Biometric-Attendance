import pymysql
import os
import requests
import time
import sqlite3
import os

def enroll_fingerprint_via_wifi(employee_id, employee_name, max_retries=3):
    """
    Send command to ESP8266 to enroll fingerprint for given employee ID and name
    """
    base_ip = os.getenv("AP_WIFI")
    if not base_ip:
        return False, "Missing AP_WIFI environment variable"
    
    base_url = f"http://{base_ip.strip()}"
    endpoint = "/enroll"
    
    for attempt in range(max_retries):
        try:
            response = requests.post(
                f"{base_url}{endpoint}",
                json={"id": int(employee_id), "name": employee_name},
                timeout=30
            )
            
            if response.status_code == 200:
                return True, "Fingerprint enrollment started successfully"
            else:
                return False, f"Device error: {response.text}"
                
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                return False, f"Connection failed: {str(e)}"
            time.sleep(2)

def add_employee(ID, Name):
    """Adds a new employee to the SQLite database and initiates fingerprint enrollment"""
    # Input validation
    if not str(ID).isdigit():
        return False, "ID must be an integer"
    if not Name.strip():
        return False, "Name cannot be empty"

    conn = None
    try:
        # Connect to SQLite database
        DB_PATH = os.path.join("C:/Users/Krypton/Desktop/projects/Biometric Attendance/config/mydb.sqlite")
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Check if ID exists
        cursor.execute("SELECT 1 FROM employee WHERE ID = ?", (ID,))
        if cursor.fetchone():
            return False, "ID already exists"

        # Insert new employee
        cursor.execute(
            "INSERT INTO employee (ID, Name) VALUES (?, ?)",
            (ID, Name.strip())
        )
        conn.commit()

        # Initiate fingerprint enrollment
        success, message = enroll_fingerprint_via_wifi(ID, Name.strip())
        
        if success:
            return True, "Employee added and fingerprint enrollment started successfully!"
        return True, f"Employee added but fingerprint enrollment failed: {message}"
    
    except sqlite3.IntegrityError as e:
        return False, f"Database integrity error: {str(e)}"
    except sqlite3.Error as e:
        return False, f"Database error: {str(e)}"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"
    finally:
        if conn:
            conn.close()