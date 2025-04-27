# save_function.py
import os
import sqlite3
from datetime import datetime
import pandas as pd
from PyQt5.QtWidgets import QMessageBox

class SaveSystem:
    def __init__(self, ui):
        self.ui = ui  # This should be the QMainWindow instance
        self.DB_PATH = os.path.join("config", "mydb.sqlite")
        
    def save_to_excel(self, date_str=None):
        """
        Save attendance records to Excel file
        Args:
            date_str: Date string in 'YYYY-MM-DD' format. If None, saves all records
        Returns:
            bool: True if successful, False otherwise
        """
        # Get records from database
        records = self.get_records_by_date(date_str)
        if not records:
            QMessageBox.warning(None, "No Data", "No records found for the selected date")
            return False
            
        try:
            # Create DataFrame from records
            df = pd.DataFrame(records, columns=['ID', 'Employee', 'Time In', 'Status', 'Time Out', 'Date'])
            
            # Generate filename with current timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            if date_str:
                filename = f"attendance_{date_str}_{timestamp}.xlsx"
            else:
                filename = f"attendance_all_records_{timestamp}.xlsx"
            
            # Save to Excel
            df.to_excel(filename, index=False, engine='openpyxl')
            
            # Show success message with file path
            abs_path = os.path.abspath(filename)
            QMessageBox.information(None, "Success", 
                                  f"Records saved to:\n{abs_path}")
            return True
            
        except Exception as e:
            QMessageBox.critical(None, "Error", 
                               f"Failed to save Excel file: {str(e)}")
            return False

    def get_records_by_date(self, date_str=None):
        """
        Fetch attendance records from database
        Args:
            date_str: Optional date filter (YYYY-MM-DD format)
        Returns:
            list: List of attendance records
        """
        conn = None
        try:
            conn = sqlite3.connect(self.DB_PATH)
            cursor = conn.cursor()

            if date_str:
                # Get records for specific date
                cursor.execute("""
                    SELECT a.id, e.name, a.time_in, a.status, a.time_out, a.date 
                    FROM attendance a
                    JOIN employee e ON a.employee_id = e.id
                    WHERE a.date = ?
                    ORDER BY a.time_in
                """, (date_str,))
            else:
                # Get all records if no date specified
                cursor.execute("""
                    SELECT a.id, e.name, a.time_in, a.status, a.time_out, a.date 
                    FROM attendance a
                    JOIN employee e ON a.employee_id = e.id
                    ORDER BY a.date, a.time_in
                """)
            
            return cursor.fetchall()

        except sqlite3.Error as e:
            raise Exception(f"Database error: {str(e)}")
        finally:
            if conn:
                conn.close() 