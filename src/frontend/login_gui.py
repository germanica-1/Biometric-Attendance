import sys
from PyQt5.QtWidgets import (
     QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, 
)
import os
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from src.backend.login_service import (
    loginuser,
) 
from src.frontend.forgot_passwrod_gui import ResetPasswordPanel

class LoginPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        if getattr(sys, "frozen", False): 
            self.BASE_DIR = (
                sys._MEIPASS 
            )
 
    def initUI(self):
        self.setWindowTitle('Login Page')
        self.setFixedSize(350, 270)  
        
        # Title Label
        title = QLabel('ADMIN LOGIN', self)
        title.setFont(QFont('Arial', 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        
        # Username Label and Input
        user_label = QLabel('Username:')
        user_label.setFont(QFont('Times New Roman', 15))
        self.user_input = QLineEdit()
        self.user_input.setFixedSize(320, 30)
        self.user_input.setFont(QFont('Times New Roman', 15))
        
        # Password Label and Input
        pass_label = QLabel('Password:')
        pass_label.setFont(QFont('Times New Roman', 15))
        self.pass_input = QLineEdit()
        self.pass_input.setFixedSize(320, 30)
        self.pass_input.setFont(QFont('Times New Roman', 15))
        
        # Forgot Password Section
        forgot_label = QLabel('Forgot Password?')
        forgot_label.setFont(QFont('Times New Roman', 13))
        reset_btn = QPushButton('Reset')
        reset_btn.setFont(QFont('Times New Roman', 10))
        reset_btn.setFixedSize(80, 30)
        
        forgot_layout = QHBoxLayout()
        forgot_layout.addStretch()
        forgot_layout.addWidget(forgot_label)
        forgot_layout.addWidget(reset_btn)
        forgot_layout.addStretch()
        reset_btn.clicked.connect(self.open_forgot_password)  # Connect to login function
        
        # Submit Button
        submit_btn = QPushButton('LOGIN')
        submit_btn.setFont(QFont('Arial', 12, QFont.Bold))
        submit_btn.setFixedSize(150, 40)
        submit_btn.clicked.connect(self.handle_login)  # Connect to login function
        
        # Layout
        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(user_label)
        layout.addWidget(self.user_input)
        layout.addWidget(pass_label)
        layout.addWidget(self.pass_input)
        layout.addLayout(forgot_layout)
        layout.addStretch()
        layout.addWidget(submit_btn, alignment=Qt.AlignCenter)
        layout.addStretch()
        
        self.setLayout(layout)
        
        # Disable Maximize Button
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)

    def handle_login(self):
        username = self.user_input.text()
        password = self.pass_input.text()
        # Calls the backend function
        loginuser(username, password, self)        

    def open_forgot_password(self):
        """Function to open the forgot password window"""
        self.ui = ResetPasswordPanel() 
        self.ui.show() #show window


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginPanel()
    window.show()
    sys.exit(app.exec_())