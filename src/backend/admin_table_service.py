import os
import pymysql
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox

import sqlite3
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem

def load_data(tableWidget):
    """Fetch and display admin data while excluding the password column."""
    DB_PATH = os.path.join("config", "mydb.sqlite")
    
    conn = None
    try:
        # Connect to SQLite database
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  # Enable dictionary-style access
        cursor = conn.cursor()

        # Get column names (excluding password)
        cursor.execute("PRAGMA table_info(login)")
        columns = [column[1] for column in cursor.fetchall() 
                  if column[1].lower() != 'password']
        
        # Set table columns
        tableWidget.setColumnCount(len(columns))
        tableWidget.setHorizontalHeaderLabels(columns)

        # Fetch data
        query = "SELECT user, Username, pin_admin FROM login"  # Explicit columns
        cursor.execute(query)
        results = cursor.fetchall()

        # Return as list of rows that can be indexed
        return list(results)

    except sqlite3.Error as err:
        QMessageBox.critical(None, "Database Error", f"Failed to fetch data: {str(err)}")
        return None
    finally:
        if conn:
            conn.close()

def remove_admin(username, load_data_callback=None):
    """Function to remove an admin by username using SQLite."""
    DB_PATH = os.path.join("config", "mydb.sqlite")
    username = username.strip()
    
    if not username:
        QMessageBox.warning(None, "Input Error", "Please enter a username to remove.")
        return

    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Check if username exists
        cursor.execute("SELECT * FROM login WHERE Username = ?", (username,))
        user = cursor.fetchone()
        
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
            cursor.execute("DELETE FROM login WHERE Username = ?", (username,))
            conn.commit()
            QMessageBox.information(None, "Success", f"Admin '{username}' removed successfully.")
            
            # Refresh the data if a callback is provided
            if load_data_callback:
                load_data_callback()

    except sqlite3.Error as err:
        QMessageBox.critical(None, "Database Error", f"An error occurred: {str(err)}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()