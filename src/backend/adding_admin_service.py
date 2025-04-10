import pymysql
import os


def add_admin(user_id, username, password, pin):
    if not user_id.isdigit():
        return False, "UserID must be an integer"
    if not username or not password:
        return False, "Username and Password cannot be empty"
    if not pin.isdigit() or len(pin) != 4:
        return False, "Admin Pin must be a 4-digit number"
    
    # Initialize variables to None
    mydb = None
    cursor = None
    
    try:
        # Hash the password with passlib
        from passlib.hash import pbkdf2_sha256  # Using PBKDF2 with SHA256
        hashed_password = pbkdf2_sha256.hash(password)
        
        mydb = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            cursorclass=pymysql.cursors.DictCursor
        )
        cursor = mydb.cursor()

        # Check if the user ID already exists
        cursor.execute("SELECT * FROM login WHERE user = %s", (user_id,))
        if cursor.fetchone():
            return False, "UserID already exists"

        # Insert with hashed password
        cursor.execute(
            "INSERT INTO login (user, Username, Password, pin_admin) VALUES (%s, %s, %s, %s)",
            (user_id, username, hashed_password, pin)
        )
        mydb.commit()
        return True, "Admin added successfully!"
    
    except Exception as e:
        # Rollback in case of error
        if mydb:
            mydb.rollback()
        return False, f"Database Error: {str(e)}"
    finally:
        # Close cursor if it exists
        if cursor:
            cursor.close()
        # Close connection if it exists
        if mydb:
            mydb.close()