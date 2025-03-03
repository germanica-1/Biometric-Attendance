import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from src.backend.adding_admin_service import add_admin



class AddAdminPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Add New Admin')
        self.setFixedSize(350, 370)  # Set a fixed window size

        # Title Label
        title = QLabel('NEW ADMIN', self)
        title.setFont(QFont('Arial', 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        # UserID
        user_id_label = QLabel('UserID:')
        user_id_label.setFont(QFont('Times New Roman', 12))
        self.user_id_input = QLineEdit()
        self.user_id_input.setFixedSize(320, 30)
        self.user_id_input.setFont(QFont('Times New Roman', 15))
        self.user_id_input.setPlaceholderText("Must be an integer and isn't used")

        # Username
        username_label = QLabel('Username:')
        username_label.setFont(QFont('Times New Roman', 12))
        self.username_input = QLineEdit()
        self.username_input.setFixedSize(320, 30)
        self.username_input.setFont(QFont('Times New Roman', 15))

        # Password
        password_label = QLabel('Password:')
        password_label.setFont(QFont('Times New Roman', 12))
        self.password_input = QLineEdit()
        self.password_input.setFixedSize(320, 30)
        self.password_input.setFont(QFont('Times New Roman', 15))

        # Admin Pin
        pin_label = QLabel('Admin Pin:')
        pin_label.setFont(QFont('Times New Roman', 12))
        self.pin_input = QLineEdit()
        self.pin_input.setFixedSize(320, 30)
        self.pin_input.setFont(QFont('Times New Roman', 15))
        self.pin_input.setPlaceholderText("Must be an integer (4)")

        # Add Button
        add_btn = QPushButton('ADD')
        add_btn.setFont(QFont('Times New Roman', 12, QFont.Bold))
        add_btn.setFixedSize(120, 40)
        add_btn.clicked.connect(self.handle_add_admin)
        

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(user_id_label)
        layout.addWidget(self.user_id_input)
        layout.addWidget(username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(pin_label)
        layout.addWidget(self.pin_input)
        layout.addWidget(add_btn, alignment=Qt.AlignCenter)
        layout.addStretch()


        self.setLayout(layout)

        # Disable Maximize Button
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)

    def handle_add_admin(self):
        user_id = self.user_id_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        pin = self.pin_input.text().strip()

        success, message = add_admin(user_id, username, password, pin)
        self.show_message('Success' if success else 'Error', message)

    def show_message(self, title, message):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AddAdminPanel()
    window.show()
    sys.exit(app.exec_())
