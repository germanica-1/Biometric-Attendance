import os
import sqlite3
from datetime import datetime
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox

class TimeOutSystem:
    def __init__(self, ui):
        self.ui = ui  # MainWindow instance
        self.DB_PATH = os.path.join("config", "mydb.sqlite")
            
    def time_out_employee(self, employee_name, manual_time=None):
        """Handle employee time-out process with proper duplicate prevention"""
        main_window = self.ui if isinstance(self.ui, QtWidgets.QMainWindow) else None
        
        if not employee_name:
            QMessageBox.warning(main_window, "Input Error", "Please enter an employee name")
            return False

        # Get current date
        current_date = datetime.now().strftime("%Y-%m-%d")
        emp_id = None
        existing_time_out = None
        
        # First check all conditions in a single database transaction
        conn = None
        try:
            conn = sqlite3.connect(self.DB_PATH)
            cursor = conn.cursor()
            
            # Get employee ID with row locking to prevent race conditions
            cursor.execute("SELECT id FROM employee WHERE name = ?", (employee_name,))
            employee = cursor.fetchone()
            
            if not employee:
                QMessageBox.warning(main_window, "Not Found", "Employee not found")
                return False
                
            emp_id = employee[0]
            
            # Get complete attendance record for today with locking
            cursor.execute("""
                SELECT time_in, time_out FROM attendance 
                WHERE employee_id = ? AND date = ?
                LIMIT 1 FOR UPDATE
            """, (emp_id, current_date))
            
            record = cursor.fetchone()
            
            if not record:
                QMessageBox.warning(main_window, "No Record", 
                                "Employee has no attendance record for today")
                return False
                
            time_in, existing_time_out = record
            
            if not time_in:
                QMessageBox.warning(main_window, "No Time In", 
                                "Employee hasn't timed in today")
                return False
                
            if existing_time_out is not None:
                QMessageBox.warning(main_window, "Already Timed Out", 
                                f"{employee_name} already timed out at {existing_time_out}")
                return False
                
            # Only show confirmation if all checks passed
            confirm = QMessageBox.question(
                main_window,
                "Confirm Time Out",
                f"Are you sure you want to time out {employee_name}?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if confirm != QMessageBox.Yes:
                conn.rollback()
                return False  # User cancelled

            # Get current time (or use manual time)
            now = datetime.now()
            if manual_time:
                current_time = manual_time
                try:
                    # Validate manual time format
                    datetime.strptime(f"{current_date} {manual_time}", "%Y-%m-%d %I:%M %p")
                except ValueError:
                    conn.rollback()
                    QMessageBox.warning(main_window, "Time Error", 
                                    "Invalid manual time format (use HH:MM AM/PM)")
                    return False
            else:
                current_time = now.strftime("%I:%M %p")

            # Update time-out record with additional verification
            cursor.execute("""
                UPDATE attendance 
                SET time_out = ?
                WHERE employee_id = ? AND date = ? AND time_out IS NULL
                RETURNING time_out
            """, (current_time, emp_id, current_date))
            
            updated_record = cursor.fetchone()
            
            if not updated_record:
                conn.rollback()
                QMessageBox.warning(main_window, "Error", 
                                "Could not update time-out - record may have changed")
                return False
                
            conn.commit()
            
            # Update UI if available
            if hasattr(self.ui, 'EmployeeTable'):
                self.update_attendance_table()
            
            QMessageBox.information(main_window, "Success",
                                f"{employee_name} timed out at {current_time}")
            return True
            
        except sqlite3.Error as e:
            if conn:
                conn.rollback()
            QMessageBox.critical(main_window, "Database Error",
                            f"Failed to record time-out: {str(e)}")
            return False
        finally:
            if conn:
                conn.close()

    def update_attendance_table(self):
        """Refresh the attendance table in UI sorted by employee ID"""
        conn = None
        try:
            conn = sqlite3.connect(self.DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT a.id, e.name, a.time_in, a.status, a.time_out, a.date
                FROM attendance a
                JOIN employee e ON a.employee_id = e.id
                ORDER BY a.employee_id ASC
            """)
            
            results = cursor.fetchall()
            table = self.ui.EmployeeTable
            table.setRowCount(len(results))
            table.setColumnCount(6)
            
            for row_idx, row_data in enumerate(results):
                for col_idx, col_data in enumerate(row_data):
                    item = QtWidgets.QTableWidgetItem(str(col_data if col_data is not None else ""))
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    table.setItem(row_idx, col_idx, item)
                    
        except sqlite3.Error as e:
            QMessageBox.critical(self.ui, "Database Error",
                               f"Failed to load attendance: {str(e)}")
        finally:
            if conn:
                conn.close()
