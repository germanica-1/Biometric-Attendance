import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, 
    QVBoxLayout, QHBoxLayout, QComboBox, QFrame, QMainWindow
)
from PyQt5.QtGui import QFont, QRegExpValidator
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtWidgets import QMessageBox
from src.backend.time_in import TimeInSystem  # Import your TimeInSystem class

class TimeEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMaxLength(5)
        self.setPlaceholderText("HH:MM")
        self.setFont(QFont('Times New Roman', 15))
        self.setFixedSize(220, 30)
        
        # Set validator to only allow digits and colon in correct positions
        regex = QRegExp("^(0[0-9]|1[0-2]):[0-5][0-9]$")
        validator = QRegExpValidator(regex, self)
        self.setValidator(validator)
        
    def keyPressEvent(self, event):
        # Auto-insert colon after first two digits
        text = self.text()
        if len(text) == 2 and event.key() not in (Qt.Key_Backspace, Qt.Key_Delete):
            super().keyPressEvent(event)
            self.setText(text + ":")
            self.setCursorPosition(3)
        else:
            super().keyPressEvent(event)

class EmployeeTimeInPanel(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_ui = parent  # Reference to the main window
        self.time_in_system = TimeInSystem(self.parent_ui)  # Initialize with parent UI
        self.setupUI()
    
    def setupUI(self):
        self.setWindowTitle('Time in Employee')
        self.setFixedSize(400, 280)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main layout
        main_layout = QVBoxLayout(self.central_widget)
        
        # Title Label
        title = QLabel('Time in Employee')
        title.setFont(QFont('Arial', 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # Employee Name Section
        name_label = QLabel('Employee Name:')
        name_label.setFont(QFont('Times New Roman', 15))
        
        self.name_input = QLineEdit()
        self.name_input.setFont(QFont('Times New Roman', 15))
        self.name_input.setFixedSize(360, 30)
        self.name_input.setPlaceholderText("Enter employee name")

        # Time In Section
        time_in_label = QLabel('Time in:')
        time_in_label.setFont(QFont('Times New Roman', 15))
        
        self.time_in_input = TimeEdit()
        self.time_in_input.setFixedSize(280, 30)
        self.time_in_ampm = QComboBox()
        self.time_in_ampm.addItems(["AM", "PM"])
        self.time_in_ampm.setFont(QFont('Times New Roman', 12))
        self.time_in_ampm.setFixedSize(80, 30)
        
        time_in_layout = QHBoxLayout()
        time_in_layout.addWidget(self.time_in_input)
        time_in_layout.addWidget(self.time_in_ampm)
        time_in_layout.addStretch()

        # Set Button
        set_btn = QPushButton('Set')
        set_btn.setFont(QFont('Arial', 12, QFont.Bold))
        set_btn.setFixedSize(150, 40)
        set_btn.clicked.connect(self.handle_time_in)

        # Status label
        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignCenter)

        # Add widgets to main layout
        main_layout.addSpacing(10)
        main_layout.addWidget(name_label)
        main_layout.addWidget(self.name_input)
        main_layout.addSpacing(10)
        main_layout.addWidget(time_in_label)
        main_layout.addLayout(time_in_layout)
        main_layout.addStretch()
        main_layout.addWidget(set_btn, alignment=Qt.AlignCenter)
        main_layout.addSpacing(10)
        main_layout.addWidget(self.status_label)
        main_layout.addStretch()

    def handle_time_in(self):
        """Handle the manual time-in process"""
        employee_name = self.name_input.text().strip()
        time_text = self.time_in_input.text()
        ampm = self.time_in_ampm.currentText()
        
        # Validate inputs
        if not employee_name:
            QMessageBox.warning(self, "Error", "Please enter employee name.")
            return
            
        if not time_text:
            QMessageBox.warning(self, "Error", "Please enter time in value.")
            return
            
        try:
            # Validate time format
            hours, minutes = map(int, time_text.split(':'))
            if hours < 1 or hours > 12 or minutes < 0 or minutes > 59:
                raise ValueError
                
            # Format the time with AM/PM
            formatted_time = f"{time_text} {ampm}"
            
            # Call the time_in_employee method with both parameters
            success = self.time_in_system.time_in_employee(
                employee_name=employee_name,
                manual_time=formatted_time
            )
            
            if success:
                self.status_label.setText(f"Time out recorded: {employee_name} at {formatted_time}")
                
                
        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter a valid time in HH:MM format (e.g., 08:30).")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = EmployeeTimeInPanel()
    window.show()
    sys.exit(app.exec_())