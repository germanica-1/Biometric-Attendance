import sys
import json
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, 
    QVBoxLayout, QHBoxLayout, QComboBox, QFrame
)
from PyQt5.QtGui import QFont, QRegExpValidator
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtWidgets import QMessageBox

# Constants
CONFIG_FILE = "work_times.json"

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

class SetWorkTimePanel(QWidget):
    def __init__(self):
        super().__init__()
        self.current_time_in = None
        self.current_time_out = None
        self.load_times()  # Load saved times when initializing
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Set Work Time')
        self.setFixedSize(400, 350)

        # Main layout
        main_layout = QVBoxLayout()
        
        # Title Label
        title = QLabel('Set Work Time')
        title.setFont(QFont('Arial', 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

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

        # Time Out Section
        time_out_label = QLabel('Time out:')
        time_out_label.setFont(QFont('Times New Roman', 15))
        
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

        # Set Button
        set_btn = QPushButton('Set')
        set_btn.setFont(QFont('Arial', 12, QFont.Bold))
        set_btn.setFixedSize(150, 40)
        set_btn.clicked.connect(self.on_set_button_clicked)  

        # Status display
        status_frame = QFrame()
        status_frame.setFrameShape(QFrame.StyledPanel)
        status_frame.setFixedHeight(50)
        status_layout = QVBoxLayout(status_frame)
        status_layout.setContentsMargins(10, 5, 10, 5)
        
        self.status_label = QLabel("No times set")
        self.status_label.setFont(QFont('Arial', 10))
        self.status_label.setAlignment(Qt.AlignCenter)
        status_layout.addWidget(self.status_label)

        # Add widgets to main layout
        main_layout.addSpacing(10)
        main_layout.addWidget(time_in_label)
        main_layout.addLayout(time_in_layout)
        main_layout.addSpacing(10)
        main_layout.addWidget(time_out_label)
        main_layout.addLayout(time_out_layout)
        main_layout.addStretch()
        main_layout.addWidget(set_btn, alignment=Qt.AlignCenter)
        main_layout.addSpacing(10)
        main_layout.addWidget(status_frame)
        main_layout.addStretch()

        self.setLayout(main_layout)
        self.update_status_display()  # Update display with loaded times

    def load_times(self):
        """Load saved times from file if exists"""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    data = json.load(f)
                    self.current_time_in = data.get('time_in')
                    self.current_time_out = data.get('time_out')
            except Exception as e:
                self.current_time_in = None
                self.current_time_out = None

    def save_times(self):
        """Save current times to file"""
        if self.current_time_in and self.current_time_out:
            try:
                with open(CONFIG_FILE, 'w') as f:
                    json.dump({
                        'time_in': self.current_time_in,
                        'time_out': self.current_time_out
                    }, f)
            except Exception as e:
                print(f"Error saving times: {e}")

    def update_status_display(self):
        """Update the status display with current times"""
        if self.current_time_in and self.current_time_out:
            status_text = f"Current Time:\nIn: {self.current_time_in} | Out: {self.current_time_out}"
        else:
            status_text = "No times set"
        self.status_label.setText(status_text)

    def on_set_button_clicked(self):
        time_in = self.time_in_input.text()
        time_out = self.time_out_input.text()
        ampm_in = self.time_in_ampm.currentText()
        ampm_out = self.time_out_ampm.currentText()

        if not time_in or not time_out:
            QMessageBox.warning(self, "Input Error", "Both time fields are required.")
            return

        if not self.validate_time_format(time_in) or not self.validate_time_format(time_out):
            QMessageBox.warning(self, "Input Error", 
                              "Please enter valid times in HH:MM format (e.g., 08:30)")
            return

        # Convert to 24-hour format for comparison
        time_in_24hr = self.convert_to_24hr(time_in, ampm_in)
        time_out_24hr = self.convert_to_24hr(time_out, ampm_out)
        
        if time_out_24hr <= time_in_24hr:
            QMessageBox.warning(self, "Input Error", "Time out must be after Time in")
            return

        # Store the current times
        self.current_time_in = f"{time_in} {ampm_in}"
        self.current_time_out = f"{time_out} {ampm_out}"
        
        # Save to file
        self.save_times()
        
        # Update the status display
        self.update_status_display()

        # Show success message
        QMessageBox.information(self, "Success", 
                              f"Work times set and saved!\n"
                              f"Time In: {self.current_time_in}\n"
                              f"Time Out: {self.current_time_out}")
        
        # Clear input fields
        self.time_in_input.clear()
        self.time_out_input.clear()
        self.time_in_ampm.setCurrentIndex(0)
        self.time_out_ampm.setCurrentIndex(0)
        
    def validate_time_format(self, time_str):
        """Validate the time format (HH:MM)"""
        if len(time_str) != 5 or time_str[2] != ':':
            return False
        
        try:
            hours, minutes = map(int, time_str.split(':'))
            return 1 <= hours <= 12 and 0 <= minutes < 60
        except ValueError:
            return False
    
    def convert_to_24hr(self, time_str, ampm):
        """Convert 12-hour format to minutes for comparison"""
        hours, minutes = map(int, time_str.split(':'))
        if ampm == "PM" and hours != 12:
            hours += 12
        elif ampm == "AM" and hours == 12:
            hours = 0
        return hours * 60 + minutes

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SetWorkTimePanel()
    window.show()
    sys.exit(app.exec_())