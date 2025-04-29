import os
import sqlite3
import json
import threading
import time  # This is the correct time module for sleep
from datetime import datetime  # Only import datetime from datetime module
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox
from flask import Flask, request, jsonify, current_app
from werkzeug.serving import make_server
import re
import socket


class TimeInSystem:
    def __init__(self, ui):
        self.ui = ui  # MainWindow instance
        self.DB_PATH = os.path.join("config", "mydb.sqlite")
        self.WORK_TIMES_FILE = "work_times.json"
        self.flask_app = None
        self.flask_thread = None
        self.server = None
        self.server_ready = False
        self.start_flask_server()

    def start_flask_server(self):
        """Start Flask server with proper readiness handling"""
        self.flask_app = Flask(__name__)
        
        # Store system reference in app context
        self.flask_app.config['time_system'] = self

        @self.flask_app.route('/time_in', methods=['POST', 'OPTIONS'])
        @self.flask_app.route('/time_in/', methods=['POST', 'OPTIONS'])
        # In your Flask startup:

        def handle_time_in():
            try:
                if not self.server_ready:
                    return jsonify({
                        "status": "error", 
                        "message": "Server not ready yet"
                    }), 503

                # Debug: Print complete request info
                print(f"\n=== Incoming Request ===")
                print(f"Method: {request.method}")
                print(f"Path: {request.path}")
                print(f"Headers: {dict(request.headers)}")
                print(f"Raw data: {request.data}")
                
                # Handle OPTIONS for CORS
                if request.method == 'OPTIONS':
                    response = jsonify({'status': 'success'})
                    response.headers.add('Access-Control-Allow-Origin', '*')
                    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
                    return response

                if not request.is_json:
                    print("Request is not JSON")
                    return jsonify({"status": "error", "message": "Request must be JSON"}), 400

                data = request.get_json()
                print("Processing time in/out request:", data)

                # Validate required fields
                required = ['finger_id', 'time', 'date', 'is_time_in']
                if not all(k in data for k in required):
                    print("Missing required fields")
                    return jsonify({"status": "error", "message": "Missing required fields"}), 400

                finger_id = data['finger_id']
                time_str = data['time']
                date_str = data['date']
                is_time_in = data['is_time_in']

                # Validate time format (HH:MM AM/PM)
                if not re.match(r'^\d{1,2}:\d{2} (AM|PM)$', time_str, re.IGNORECASE):
                    return jsonify({"status": "error", "message": "Invalid time format. Use HH:MM AM/PM"}), 400

                # Validate date format (DD/MM/YYYY)
                if not re.match(r'^\d{2}/\d{2}/\d{4}$', date_str):
                    return jsonify({"status": "error", "message": "Invalid date format. Use DD/MM/YYYY"}), 400

                # Convert date to SQL format
                try:
                    day, month, year = date_str.split('/')
                    sql_date = f"{year}-{month}-{day}"
                except:
                    return jsonify({"status": "error", "message": "Invalid date components"}), 400

                # Database operations
                time_system = current_app.config['time_system']
                conn = sqlite3.connect(time_system.DB_PATH)
                cursor = conn.cursor()

                try:
                    # Get employee
                    cursor.execute("SELECT id, name FROM employee WHERE fingerprint_id = ?", (finger_id,))
                    employee = cursor.fetchone()
                    
                    if not employee:
                        return jsonify({"status": "error", "message": "Employee not found"}), 404

                    emp_id, emp_name = employee

                    if is_time_in:
                        # Time-in logic
                        cursor.execute("""
                            SELECT time_in FROM attendance 
                            WHERE employee_id = ? AND date = ? AND time_in IS NOT NULL
                        """, (emp_id, sql_date))
                        
                        if existing := cursor.fetchone():
                            return jsonify({
                                "status": "error", 
                                "message": f"{emp_name} already timed in at {existing[0]}"
                            }), 409

                        # Determine status (On Time/Late)
                        status = "On Time"
                        work_time_in, _ = time_system.get_work_times()
                        if work_time_in:
                            try:
                                work_time = datetime.strptime(work_time_in, "%I:%M %p").time()
                                current_time = datetime.strptime(time_str, "%I:%M %p").time()
                                if current_time > work_time:
                                    status = "Late"
                            except ValueError:
                                pass  # Default to "On Time"

                        # Insert record
                        cursor.execute("""
                            INSERT INTO attendance (employee_id, time_in, status, date)
                            VALUES (?, ?, ?, ?)
                        """, (emp_id, time_str, status, sql_date))
                        
                        message = f"{emp_name} timed in at {time_str}"
                    else:
                        # Time-out logic
                        cursor.execute("""
                            SELECT time_out FROM attendance 
                            WHERE employee_id = ? AND date = ? AND time_in IS NOT NULL
                        """, (emp_id, sql_date))
                        
                        if not (existing := cursor.fetchone()):
                            return jsonify({
                                "status": "error", 
                                "message": f"{emp_name} must time in before timing out"
                            }), 400
                            
                        if existing[0]:  # Time-out exists
                            return jsonify({
                                "status": "error", 
                                "message": f"{emp_name} already timed out today"
                            }), 409
                        
                        cursor.execute("""
                            UPDATE attendance
                            SET time_out = ?
                            WHERE employee_id = ? AND date = ? AND time_in IS NOT NULL AND time_out IS NULL
                        """, (time_str, emp_id, sql_date))
                        
                        message = f"{emp_name} timed out at {time_str}"

                    conn.commit()

                    # Update UI if available
                    if hasattr(time_system.ui, 'update_attendance_table'):
                        time_system.ui.update_attendance_table()


                    response = jsonify({
                        "status": "success",
                        "message": message,
                        "employee_name": emp_name,
                        "time": time_str,
                        "date": date_str
                    })
                    response.headers.add('Access-Control-Allow-Origin', '*')
                    return response, 200

                except sqlite3.Error as e:
                    conn.rollback()
                    print(f"Database error: {str(e)}")
                    return jsonify({"status": "error", "message": "Database operation failed"}), 500
                finally:
                    if conn:
                        conn.close()
                        
            except Exception as e:
                print(f"Error processing request: {str(e)}")
                return jsonify({"status": "error", "message": "Internal server error"}), 500

        @self.flask_app.route('/health')
        def health_check():
            return jsonify({
                "status": "ready" if self.server_ready else "starting",
                "server": "Biometric Attendance System"
            }), 200

        # Create server but don't run it yet
        self.server = make_server('0.0.0.0', 5000, self.flask_app)
        
        def run_server():
            print("\nStarting Flask server...")
            print(f"Server will run on: {socket.gethostbyname(socket.gethostname())}") 
            self.server_ready = True
            print("Server is now ready to accept requests")
            print("Registered routes:")
            for rule in sorted(self.flask_app.url_map.iter_rules(), key=lambda r: r.rule):
                print(f"{', '.join(rule.methods):<20} {rule.rule}")
            self.server.serve_forever()

        self.flask_thread = threading.Thread(target=run_server)
        self.flask_thread.daemon = True
        self.flask_thread.start()
        
        # Wait briefly to ensure server starts
        time.sleep(1)
        print("\nFlask server ready at http://192.168.4.2:5000")

    def stop_flask_server(self):
        """Properly shutdown the Flask server"""
        if hasattr(self, 'server'):
            print("\nShutting down Flask server...")
            self.server_ready = False
            self.server.shutdown()
            self.flask_thread.join()
            print("Flask server stopped")

    def date_records(self):
        """Open date of records"""
        from src.frontend.date_records import DateRecordsUI
        self.date_records_ui = DateRecordsUI(self) 
        self.date_records_ui.show()
        
    def get_work_times(self):
        """Get configured work times from JSON file"""
        try:
            if os.path.exists(self.WORK_TIMES_FILE):
                with open(self.WORK_TIMES_FILE, 'r') as f:
                    data = json.load(f)
                    return data.get('time_in'), data.get('time_out')
            return None, None
        except Exception as e:
            print(f"Error loading work times: {e}")
            return None, None

    def mark_absent_employees(self):
        """
        Mark employees who didn't time in/out as absent for current day
        Returns: (bool) True if successful, False otherwise
        """
        conn = None
        try:
            conn = sqlite3.connect(self.DB_PATH)
            cursor = conn.cursor()
            current_date = datetime.now().strftime("%Y-%m-%d")
            
            # Get all active employees
            cursor.execute("SELECT id FROM employee WHERE active = 1")
            active_employees = [row[0] for row in cursor.fetchall()]
            
            if not active_employees:
                return True  # No active employees to mark
                
            # Get employees with attendance records today
            cursor.execute("""
                SELECT DISTINCT employee_id FROM attendance 
                WHERE date = ? AND (time_in IS NOT NULL OR status != 'Absent')
            """, (current_date,))
            present_employees = [row[0] for row in cursor.fetchall()]
            
            # Find absent employees (active but not present)
            absent_employees = set(active_employees) - set(present_employees)
            
            # Mark absentees
            for emp_id in absent_employees:
                # Check if absent record already exists
                cursor.execute("""
                    SELECT 1 FROM attendance 
                    WHERE employee_id = ? AND date = ? AND status = 'Absent'
                """, (emp_id, current_date))
                
                if not cursor.fetchone():
                    cursor.execute("""
                        INSERT INTO attendance 
                        (employee_id, status, date) 
                        VALUES (?, ?, ?)
                    """, (emp_id, "Absent", current_date))
            
            conn.commit()
            
            # Refresh UI if available
            if hasattr(self.ui, 'EmployeeTable'):
                self.update_attendance_table()
                
            return True
            
        except sqlite3.Error as e:
            QMessageBox.critical(self.ui, "Database Error", 
                               f"Failed to mark absent employees: {str(e)}")
            return False
        finally:
            if conn:
                conn.close()

    def check_and_mark_absentees(self):
        """
        Automatically mark absent employees after work hours
        Returns: (bool) True if absentees were marked, False otherwise
        """
        _, work_time_out = self.get_work_times()
        
        if not work_time_out:
            return False
            
        try:
            # Parse work end time
            end_time = datetime.strptime(work_time_out, "%I:%M %p").time()
            current_time = datetime.now().time()
            
            # Only mark absent if work day has ended
            if current_time > end_time:
                return self.mark_absent_employees()
            return False
        except ValueError as e:
            print(f"Error parsing work times: {e}")
            return False

    def time_in_employee(self, employee_name, manual_time=None):
        """Handle employee time-in process with required employee_name"""
        main_window = self.ui if isinstance(self.ui, QtWidgets.QMainWindow) else None
        
        if not employee_name:
            QMessageBox.warning(main_window, "Input Error", "Please enter an employee name")
            return False

        # Get current date
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # First check if employee exists and has already timed in
        conn = None
        try:
            conn = sqlite3.connect(self.DB_PATH)
            cursor = conn.cursor()
            
            # Get employee ID
            cursor.execute("SELECT id FROM employee WHERE name = ?", (employee_name,))
            employee = cursor.fetchone()
            
            if not employee:
                QMessageBox.warning(main_window, "Not Found", "Employee not found")
                return False
                
            emp_id = employee[0]
            
            # Check for existing time-in record
            cursor.execute("""
                SELECT time_in FROM attendance 
                WHERE employee_id = ? AND date = ? AND time_in IS NOT NULL
            """, (emp_id, current_date))
            
            existing_time = cursor.fetchone()
            if existing_time:
                QMessageBox.warning(main_window, "Already Timed In", 
                                f"{employee_name} has already timed in today at {existing_time[0]}")
                return False
                
        except sqlite3.Error as e:
            QMessageBox.critical(main_window, "Database Error",
                            f"Error checking employee status: {str(e)}")
            return False
        finally:
            if conn:
                conn.close()

        # Only show confirmation if employee hasn't timed in yet
        confirm = QMessageBox.question(
            main_window,
            "Confirm Time In",
            f"Are you sure you want to time in {employee_name}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if confirm != QMessageBox.Yes:
            return False  # User cancelled
            
        # Get current time (or use manual time)
        now = datetime.now()
        if manual_time:
            current_time = manual_time
            try:
                now = datetime.strptime(f"{current_date} {manual_time}", "%Y-%m-%d %I:%M %p")
            except ValueError:
                QMessageBox.warning(main_window, "Time Error", "Invalid manual time format")
                return False
        else:
            current_time = now.strftime("%I:%M %p")

        # Determine status
        status = "On Time"
        work_time_in, _ = self.get_work_times()
        if work_time_in:
            try:
                work_time = datetime.strptime(work_time_in, "%I:%M %p").time()
                if now.time() > work_time:
                    status = "Late"
            except ValueError:
                pass  # Default to "On Time" if comparison fails

        # Process time-in in database
        conn = None
        try:
            conn = sqlite3.connect(self.DB_PATH)
            cursor = conn.cursor()
            
            # Insert time-in record
            cursor.execute("""
                INSERT INTO attendance 
                (employee_id, time_in, status, date)
                VALUES (?, ?, ?, ?)
            """, (emp_id, current_time, status, current_date))
            
            conn.commit()
            
            if hasattr(self.ui, 'EmployeeTable'):
                self.update_attendance_table()
            
            QMessageBox.information(main_window, "Success",
                                f"{employee_name} timed in at {current_time}\n"
                                f"Status: {status}")
            return True
            
        except sqlite3.Error as e:
            QMessageBox.critical(main_window, "Database Error",
                            f"Failed to record time-in: {str(e)}")
            return False
        finally:
            if conn:
                conn.close()

    def update_attendance_table(self):
        """Refresh the attendance table in UI sorted by employee ID ascending"""
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