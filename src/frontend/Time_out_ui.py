import sys
import sqlite3
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, 
    QLineEdit, QPushButton, QVBoxLayout, 
    QHBoxLayout, QComboBox, QMessageBox
)
from PyQt5.QtGui import QFont, QRegExpValidator
from PyQt5.QtCore import Qt, QRegExp

class TimeEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMaxLength(5)
        self.setPlaceholderText("HH:MM")
        self.setFont(QFont('Times New Roman', 15))
        self.setFixedSize(220, 30)
        
        
        regex = QRegExp("^(0[0-9]|1[0-2]):[0-5][0-9]$")
        validator = QRegExpValidator(regex, self)
        self.setValidator(validator)
        
    def keyPressEvent(self, event):
        #
        text = self.text()
        if len(text) == 2 and event.key() not in (Qt.Key_Backspace, Qt.Key_Delete):
            super().keyPressEvent(event)
            self.setText(text + ":")
            self.setCursorPosition(3)
        else:
            super().keyPressEvent(event)

class EmployeeTimeOutPanel(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_ui = parent  # Reference to the main window
        self.DB_PATH = "config/mydb.sqlite"  # Database path
        self.setupUI()
    
    def setupUI(self):
        self.setWindowTitle('Time Out Employee')
        self.setFixedSize(400, 280)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main layout
        main_layout = QVBoxLayout(self.central_widget)
        
        # Title Label
        title = QLabel('Time Out Employee')
        title.setFont(QFont('Arial', 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # Employee Name Section
        name_label = QLabel('Employee Name:')
        name_label.setFont(QFont('Times New Roman', 15))
        main_layout.addWidget(name_label)
        
        self.name_input = QLineEdit()
        self.name_input.setFont(QFont('Times New Roman', 15))
        self.name_input.setFixedSize(360, 30)
        self.name_input.setPlaceholderText("Enter employee name")
        main_layout.addWidget(self.name_input)

        # Time Out Section
        time_out_label = QLabel('Time Out:')
        time_out_label.setFont(QFont('Times New Roman', 15))
        main_layout.addWidget(time_out_label)
        
        self.time_out_input = TimeEdit()
        self.time_out_input.setFixedSize(280, 30)
        self.time_out_ampm = QComboBox()
        self.time_out_ampm.addItems(["AM", "PM"])
        self.time_out_ampm.setFont(QFont('Times New Roman', 12))
        self.time_out_ampm.setFixedSize(80, 30)
        
        time_out_layout = QHBoxLayout()
        time_out_layout.addWidget(self.time_out_input)
        time_out_layout.addWidget(self.time_out_ampm)
        time_out_layout.addStretch()
        main_layout.addLayout(time_out_layout)

        # Set Button
        set_btn = QPushButton('Set Time Out')
        set_btn.setFont(QFont('Arial', 12, QFont.Bold))
        set_btn.setFixedSize(150, 40)
        set_btn.clicked.connect(self.handle_time_out)  # Connect button click
        main_layout.addWidget(set_btn, alignment=Qt.AlignCenter)

        # Status label
        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.status_label)

    def handle_time_out(self):
        """Handle the time-out process when button is clicked"""
        employee_name = self.name_input.text().strip()
        time_text = self.time_out_input.text()
        ampm = self.time_out_ampm.currentText()
        
        # Validate inputs
        if not employee_name:
            QMessageBox.warning(self, "Error", "Please enter employee name")
            return
            
        if not time_text:
            QMessageBox.warning(self, "Error", "Please enter time out value")
            return
            
        try:
            # Validate time format
            hours, minutes = map(int, time_text.split(':'))
            if hours < 1 or hours > 12 or minutes < 0 or minutes > 59:
                raise ValueError
                
            # Format the time with AM/PM
            formatted_time = f"{time_text} {ampm}"
            current_date = datetime.now().strftime("%Y-%m-%d")
            
            # Database operations
            conn = sqlite3.connect(self.DB_PATH)
            cursor = conn.cursor()
            
            # Get employee ID
            cursor.execute("SELECT id FROM employee WHERE name = ?", (employee_name,))
            employee = cursor.fetchone()
            
            if not employee:
                QMessageBox.warning(self, "Not Found", "Employee not found")
                return
                
            emp_id = employee[0]
            
            # Check if employee has timed in today
            cursor.execute("""
                SELECT id FROM attendance 
                WHERE employee_id = ? AND date = ? AND time_in IS NOT NULL
            """, (emp_id, current_date))
            
            if not cursor.fetchone():
                QMessageBox.warning(self, "No Time In", 
                                  "Employee hasn't timed in today")
                return
                
            # Update time-out record
            cursor.execute("""
                UPDATE attendance 
                SET time_out = ?
                WHERE employee_id = ? AND date = ?
            """, (formatted_time, emp_id, current_date))
            
            conn.commit()
            
        
            if self.parent_ui and hasattr(self.parent_ui, 'EmployeeTable'):
                self.parent_ui.EmployeeTable.update() 
            
            self.status_label.setText(f"Time out recorded: {employee_name} at {formatted_time}")
            QMessageBox.information(self, "Success", "Time out recorded successfully")
            
        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter a valid time in HH:MM format (e.g., 05:30 PM)")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", f"Failed to record time out: {str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = EmployeeTimeOutPanel()
    window.show()
    sys.exit(app.exec_())