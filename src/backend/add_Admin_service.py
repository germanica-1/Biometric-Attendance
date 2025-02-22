import os
import pymysql
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

def load_data(self):
    """ Fetch and display admin data in the table widget. """
    try:
        # Connect to the database using environment variables
        mydb = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            cursorclass=pymysql.cursors.DictCursor  # Fetch results as dictionaries
        )
        mycursor = mydb.cursor()
        print("Connected to database")

    except pymysql.MySQLError as err:
        print(f"Database connection error: {err}")
        QMessageBox.critical(None, "Connection Error", "Failed to connect to the database.")
        return

    try:
        # Fetch column names dynamically
        mycursor.execute("SHOW COLUMNS FROM login")
        columns = [column['Field'] for column in mycursor.fetchall()]  # 'Field' is the key for column names


        # Set column headers in the QTableWidget
        self.tableWidget.setColumnCount(len(columns))
        self.tableWidget.setHorizontalHeaderLabels(columns)

        # Execute the SQL query to fetch data
        query = "SELECT user, Username, Password, pin_admin FROM login"
        mycursor.execute(query)
        results = mycursor.fetchall()  # Fetch all rows

        # Set the number of rows in the table
        self.tableWidget.setRowCount(len(results))

        # Insert data into the table
        for row_idx, row in enumerate(results):
            for col_idx, col_name in enumerate(columns):
                self.tableWidget.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(row[col_name])))

    except pymysql.MySQLError as err:
        print(f"Error fetching data: {err}")
        QMessageBox.critical(None, "Database Error", "Failed to fetch data from the database.")

    finally:
        # Close the cursor and connection
        mycursor.close()
        mydb.close()
