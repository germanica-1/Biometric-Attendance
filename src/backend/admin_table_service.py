import os
import pymysql
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

#Refreshing and loading table database
def load_data(tableWidget):
    """ Fetch and display admin data in the table widget. """
    try:
        mydb = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            cursorclass=pymysql.cursors.DictCursor
        )
        mycursor = mydb.cursor()
        print("Connected to database")
    except pymysql.MySQLError as err:
        print(f"Database connection error: {err}")
        QMessageBox.critical(None, "Connection Error", "Failed to connect to the database.")
        return None  # Return None if connection fails

    try:
        mycursor.execute("SHOW COLUMNS FROM login")
        columns = [column['Field'] for column in mycursor.fetchall()]

        tableWidget.setColumnCount(len(columns))
        tableWidget.setHorizontalHeaderLabels(columns)

        # Fetch data
        query = "SELECT user, Username, Password, pin_admin FROM login"
        mycursor.execute(query)
        results = mycursor.fetchall()  # Fetch all rows

        tableWidget.setRowCount(len(results))

        for row_idx, row in enumerate(results):
            for col_idx, col_name in enumerate(columns):
                tableWidget.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(row[col_name])))

        return results  # Return the fetched data

    except pymysql.MySQLError as err:
        print(f"Error fetching data: {err}")
        QMessageBox.critical(None, "Database Error", "Failed to fetch data from the database.")
        return None  # Return None if query fails

    finally:
        mycursor.close()
        mydb.close()

#Removing admin users
def remove_admin(username, load_data_callback=None): 
    """Function to remove an admin by username."""
    username = username.strip()  # Ensure no accidental spaces
    
    if not username:
        QMessageBox.warning(None, "Input Error", "Please enter a username to remove.")
        return

    try:
        mydb = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            cursorclass=pymysql.cursors.DictCursor
        )
        mycursor = mydb.cursor()
    except pymysql.MySQLError:
        QMessageBox.critical(None, "Connection Error", "Failed to connect to the database.")
        return

    try:
        # Check if username exists
        mycursor.execute("SELECT * FROM login WHERE Username = %s", (username,))
        user = mycursor.fetchone()
        
        if not user:
            QMessageBox.warning(None, "Not Found", f"No admin found with username: {username}")
            return

        # Confirm deletion
        confirm = QMessageBox.question(
            None, "Confirm Deletion", 
            f"Are you sure you want to remove '{username}'?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            # Delete the user
            mycursor.execute("DELETE FROM login WHERE Username = %s", (username,))
            mydb.commit()
            QMessageBox.information(None, "Success", f"Admin '{username}' removed successfully.")
            
            # Refresh the data if a callback is provided
            if load_data_callback:
                load_data_callback()  # Call the function to refresh the UI
        
    except pymysql.MySQLError as err:
        QMessageBox.critical(None, "Database Error", f"An error occurred: {err}")
    
    finally:
        mycursor.close()
        mydb.close()