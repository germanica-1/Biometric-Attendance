import os
import sqlite3
from PyQt5.QtWidgets import QMessageBox
from passlib.hash import pbkdf2_sha256

# SQLite database path 
DB_PATH = os.path.join("config", "mydb.sqlite")

def reset_password(username, new_password, admin_pin):
    """
    Verify if the username and admin pin match in the database.
    If valid, hash and update the user's password using SQLite.
    """
    conn = None
    try:
        # Connect to SQLite database
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  
        cursor = conn.cursor()
        
        # Check if the username and admin pin match
        query = "SELECT * FROM login WHERE Username = ? AND pin_admin = ?"
        cursor.execute(query, (username, admin_pin))
        user = cursor.fetchone()
        
        if user:
            # Hash the new password
            hashed_password = pbkdf2_sha256.hash(new_password)
            
            # Update the password
            update_query = "UPDATE login SET Password = ? WHERE Username = ?"
            cursor.execute(update_query, (hashed_password, username))
            conn.commit()
            
            QMessageBox.information(None, "Success", "Password has been successfully reset.")
            return True
        else:
            QMessageBox.warning(None, "Invalid Credentials", "Username or Admin PIN is incorrect.")
            return False
            
    except sqlite3.Error as err:
        QMessageBox.critical(None, "Database Error", f"SQLite error: {str(err)}")
        return False
    except Exception as e:
        QMessageBox.critical(None, "Error", f"An unexpected error occurred: {str(e)}")
        return False
    finally:
        if conn:
            conn.close()