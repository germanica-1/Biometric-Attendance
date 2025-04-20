import pymysql
import os
import requests
import time

def enroll_fingerprint_via_wifi(employee_id, employee_name, max_retries=3):
    """
    Send command to ESP8266 to enroll fingerprint for given employee ID and name
    """
    base_url = "http://192.168.4.1"  # Default AP IP of ESP8266
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
    if not ID.isdigit():
        return False, "ID must be an integer"
    if not Name:
        return False, "Name cannot be empty"

    try:
        mydb = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            cursorclass=pymysql.cursors.DictCursor
        )
        cursor = mydb.cursor()

        # Check if the ID already exists
        cursor.execute("SELECT * FROM employee WHERE ID = %s", (ID,))
        if cursor.fetchone():
            return False, "ID already exists"

        # Insert employee record
        cursor.execute(
            "INSERT INTO employee (ID, Name) VALUES (%s, %s)",
            (ID, Name)
        )
        mydb.commit()

        # Trigger fingerprint enrollment
        success, message = enroll_fingerprint_via_wifi(ID, Name)
        
        if success:
            return True, "Employee added and fingerprint enrollment started successfully!"
        else:
            return True, f"Employee added but fingerprint enrollment failed: {message}"
    
    except Exception as e:
        return False, f"Database Error: {str(e)}"

    finally:
        cursor.close()
        mydb.close()
