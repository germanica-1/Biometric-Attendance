import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from src.backend.change_wifi_service import send_wifi_credentials  # Moved import to top

class ChangeWiFiPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Change WiFi')
        self.setFixedSize(350, 250)

        # Title Label
        title = QLabel('Change WiFi', self)
        title.setFont(QFont('Arial', 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        # WiFi Name Label and Input
        wifi_name_label = QLabel('WiFi Name:')
        wifi_name_label.setFont(QFont('Times New Roman', 15))
        self.wifi_name_input = QLineEdit()
        self.wifi_name_input.setFixedSize(320, 30)
        self.wifi_name_input.setFont(QFont('Times New Roman', 15))

        # WiFi Password Label and Input
        wifi_pass_label = QLabel('WiFi Password:')
        wifi_pass_label.setFont(QFont('Times New Roman', 15))
        self.wifi_pass_input = QLineEdit()
        self.wifi_pass_input.setFixedSize(320, 30)
        self.wifi_pass_input.setFont(QFont('Times New Roman', 15))

        # Change Button
        change_btn = QPushButton('Change')
        change_btn.setFont(QFont('Arial', 12, QFont.Bold))
        change_btn.setFixedSize(150, 40)
        change_btn.clicked.connect(self.change_wifi)  # Corrected function name

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(wifi_name_label)
        layout.addWidget(self.wifi_name_input)
        layout.addWidget(wifi_pass_label)
        layout.addWidget(self.wifi_pass_input)
        layout.addStretch()
        layout.addWidget(change_btn, alignment=Qt.AlignCenter)
        layout.addStretch()

        self.setLayout(layout)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)

    def change_wifi(self):
        """ Send new WiFi credentials to the NodeMCU. """
        wifi_name = self.wifi_name_input.text()
        wifi_pass = self.wifi_pass_input.text()

        if wifi_name and wifi_pass:
            try:
                send_wifi_credentials(wifi_name, wifi_pass)
                print("WiFi credentials sent successfully.")
            except Exception as e:
                print(f"Error sending WiFi credentials: {e}")
        else:
            print("Please enter both WiFi name and password.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ChangeWiFiPanel()
    window.show()
    sys.exit(app.exec_())
