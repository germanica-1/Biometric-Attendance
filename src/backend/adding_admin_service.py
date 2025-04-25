import sqlite3
import os
from passlib.hash import pbkdf2_sha256

# Database path - adjust this to your actual path
DB_PATH = os.path.join("C:/Users/Krypton/Desktop/projects/Biometric Attendance/config/mydb.sqlite")

def add_admin(user_id, username, password, pin):
    """Adds a new admin account to the SQLite database with proper validation"""
    # Input validation
    try:
        user_id = int(user_id)
        pin = int(pin)
    except ValueError:
        return False, "ID and Pin must be numbers"
    
    if not username or not password:
        return False, "Username and Password cannot be empty"
    if len(str(pin)) != 4:
        return False, "Admin Pin must be a 4-digit number"
    
    conn = None
    try:
        # Hash the password with 29,000 iterations (security best practice)
        hashed_password = pbkdf2_sha256.using(rounds=29000).hash(password)
        
        # Connect to database with error handling
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key constraints
        cursor = conn.cursor()

        # Check if username or ID already exists
        cursor.execute(
            "SELECT 1 FROM login WHERE user = ? OR Username = ?", 
            (user_id, username)
        )
        if cursor.fetchone():
            return False, "User ID or Username already exists"

        # Insert with transaction
        cursor.execute(
            """INSERT INTO login (user, Username, Password, pin_admin) 
            VALUES (?, ?, ?, ?)""",
            (user_id, username, hashed_password, pin)
        )
        conn.commit()
        return True, f"Admin '{username}' added successfully"
    
    except sqlite3.IntegrityError as e:
        return False, f"Database integrity error: {str(e)}"
    except sqlite3.Error as e:
        return False, f"Database error: {str(e)}"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"
    finally:
        if conn:
            conn.close()

# Example usage:
if __name__ == "__main__":
    # Test adding an admin (user_id, username, password, pin)
    result, message = add_admin(1, "admin", "securepassword123", 1234)
    print(f"Success: {result}, Message: {message}")