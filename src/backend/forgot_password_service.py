import os
import pymysql
from PyQt5.QtWidgets import QMessageBox

def reset_password(username, new_password, admin_pin):
    """
    Verify if the username and admin pin match in the database.
    If valid, update the user's password.
    """
    try:
        # Connect to the database
        mydb = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            cursorclass=pymysql.cursors.DictCursor
        )
        mycursor = mydb.cursor()
    except pymysql.MySQLError as err:
        QMessageBox.critical(None, "Connection Error", "Failed to connect to the database.")
        return False
    
    try:
        # Check if the username and admin pin match
        query = "SELECT * FROM login WHERE Username = %s AND pin_admin = %s"
        mycursor.execute(query, (username, admin_pin))
        user = mycursor.fetchone()
        
        if user:
            # Update the password for the matched username
            update_query = "UPDATE login SET Password = %s WHERE Username = %s"
            mycursor.execute(update_query, (new_password, username))
            mydb.commit()
            QMessageBox.information(None, "Success", "Password has been successfully reset.")
            return True
        else:
            QMessageBox.warning(None, "Invalid Credentials", "Username or Admin PIN is incorrect.")
            return False
    
    except pymysql.MySQLError as err:
        QMessageBox.critical(None, "Database Error", "An error occurred while updating the password.")
        return False
    
    finally:
        mycursor.close()
        mydb.close()

