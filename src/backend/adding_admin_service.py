import pymysql
import os
from PyQt5.QtWidgets import QMessageBox



def add_admin(user_id, username, password, pin):
    if not user_id.isdigit():
        return False, "UserID must be an integer"
    if not username or not password:
        return False, "Username and Password cannot be empty"
    if not pin.isdigit() or len(pin) != 4:
        return False, "Admin Pin must be a 4-digit number"
    

    try:
        mydb = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            cursorclass=pymysql.cursors.DictCursor
        )
        cursor = mydb.cursor()

        # Check if the user ID already exists in the 'login' table
        cursor.execute("SELECT * FROM login WHERE user = %s", (user_id,))
        if cursor.fetchone():
            return False, "UserID already exists"

        # Insert into the 'login' table using the correct column names
        cursor.execute(
            "INSERT INTO login (user, Username, Password, pin_admin) VALUES (%s, %s, %s, %s)",
            (user_id, username, password, pin)
        )
        mydb.commit()
        return True, "Admin added successfully!"
    
    except Exception as e:
        return False, f"Database Error: {str(e)}"

    finally:
        cursor.close()
        mydb.close()
