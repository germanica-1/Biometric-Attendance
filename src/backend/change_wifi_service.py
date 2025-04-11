import os
import requests
from dotenv import load_dotenv
from PyQt5.QtWidgets import QMessageBox, QApplication
import sys


app = QApplication(sys.argv)

# Load environment variables from .env
load_dotenv()

def show_message(title, message, is_error=False):
    """Helper function to show message boxes"""
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(message)
    if is_error:
        msg.setIcon(QMessageBox.Critical)
    else:
        msg.setIcon(QMessageBox.Information)
    msg.exec_()

def send_wifi_credentials(wifi_name, wifi_password):
    try:
        # Get the AP IP from the environment variable
        ap_ip = os.getenv("AP_WIFI")
        if not ap_ip:
            show_message("Error", "AP_WIFI environment variable is not set.", True)
            return False

        # Try connecting to the AP mode IP
        response = requests.post(
            f"http://{ap_ip}/update",
            data={"ssid": wifi_name, "password": wifi_password},
            timeout=15
        )
        
        if response.status_code == 200:
            show_message("Success", "Device will restart with new WiFi")
            return True
        else:
            show_message("Error", 
                       f"Server returned: {response.status_code}\n{response.text}", 
                       True)
            return False
            
    except Exception as e:
        show_message("Connection Failed", 
                   f"Could not connect to device:\n{str(e)}", 
                   True)
        return False