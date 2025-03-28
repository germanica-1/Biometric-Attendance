import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class ResetPasswordPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Reset Password')
        self.setFixedSize(350, 330)

        # Title Label
        title = QLabel('Reset Password', self)
        title.setFont(QFont('Arial', 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        # Username Label and Input
        user_label = QLabel('Username:')
        user_label.setFont(QFont('Times New Roman', 15))
        self.user_input = QLineEdit()
        self.user_input.setFixedSize(320, 30)
        self.user_input.setFont(QFont('Times New Roman', 15))

        # New Password Label and Input
        pass_label = QLabel('New Password:')
        pass_label.setFont(QFont('Times New Roman', 15))
        self.pass_input = QLineEdit()
        self.pass_input.setFixedSize(320, 30)
        self.pass_input.setFont(QFont('Times New Roman', 15))

        # Admin PIN Label and Input
        pin_label = QLabel('ADMIN PIN MUST MATCH USER PIN:')
        pin_label.setFont(QFont('Times New Roman', 15))
        pin_label.setAlignment(Qt.AlignCenter) 
        self.pin_input = QLineEdit()
        self.pin_input.setFixedSize(320, 30)
        self.pin_input.setFont(QFont('Times New Roman', 15))

        # Submit Button
        submit_btn = QPushButton('RESET')
        submit_btn.setFont(QFont('Arial', 12, QFont.Bold))
        submit_btn.setFixedSize(150, 40)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(user_label)
        layout.addWidget(self.user_input)
        layout.addWidget(pass_label)
        layout.addWidget(self.pass_input)
        layout.addWidget(pin_label)
        layout.addWidget(self.pin_input)
        layout.addStretch()
        layout.addWidget(submit_btn, alignment=Qt.AlignCenter)
        layout.addStretch()

        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ResetPasswordPanel()
    window.show()
    sys.exit(app.exec_())
