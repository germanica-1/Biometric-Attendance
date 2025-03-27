import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from src.backend.adding_employee_service import add_employee

class EmployeeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Add New Employee')
        self.setFixedSize(350, 230)  # Set a fixed window size

        # Title Label
        title = QLabel('New Employee', self)
        title.setFont(QFont('Arial', 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        # UserID
        user_id_label = QLabel('UserID:')
        user_id_label.setFont(QFont('Times New Roman', 12))
        self.user_id_input = QLineEdit()
        self.user_id_input.setFixedSize(320, 30)
        self.user_id_input.setFont(QFont('Times New Roman', 15))
        self.user_id_input.setPlaceholderText("Must be an integer and isn't used")

        # Employee Name
        username_label = QLabel('Name:')
        username_label.setFont(QFont('Times New Roman', 12))
        self.username_input = QLineEdit()
        self.username_input.setFixedSize(320, 30)
        self.username_input.setFont(QFont('Times New Roman', 15))

        # Add Button
        add_btn = QPushButton('ADD')
        add_btn.setFont(QFont('Times New Roman', 12, QFont.Bold))
        add_btn.setFixedSize(120, 40)
        add_btn.clicked.connect(self.handle_add_employee)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(user_id_label)
        layout.addWidget(self.user_id_input)
        layout.addWidget(username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(add_btn, alignment=Qt.AlignCenter)
        layout.addStretch()


        self.setLayout(layout)

        # Disable Maximize Button
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)

    def handle_add_employee(self):
        ID = self.user_id_input.text().strip()
        Name = self.username_input.text().strip()
 
        success, message = add_employee(ID, Name)
        self.show_message('Success' if success else 'Error', message)

    def show_message(self, title, message):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = EmployeeWindow()
    window.show()
    sys.exit(app.exec_())
