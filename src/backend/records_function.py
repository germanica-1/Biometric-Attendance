import sqlite3
import os
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

class RecordsBackend:
    def __init__(self):
        self.db_path = os.path.join("config", "mydb.sqlite")

    def get_records_by_date(self, date_str):
        """Fetch attendance records for a specific date from the database"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT a.id, e.name, a.time_in, a.status, a.time_out, a.date 
                FROM attendance a
                JOIN employee e ON a.employee_id = e.id
                WHERE a.date = ?
                ORDER BY a.time_in
            """, (date_str,))
            
            return cursor.fetchall()

        except sqlite3.Error as e:
            raise Exception(f"Database error: {str(e)}")
        finally:
            if conn:
                conn.close()