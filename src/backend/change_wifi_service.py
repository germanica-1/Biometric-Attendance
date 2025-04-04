import requests

def send_wifi_credentials(wifi_name, wifi_password):
    try:
        # Try connecting to the AP mode IP
        response = requests.post(
            "http://192.168.4.1/update",
            data={"ssid": wifi_name, "password": wifi_password},
            timeout=15  # Increased timeout
        )
        if response.status_code == 200:
            print("Success! Device will restart with new WiFi")
            return True
        else:
            print(f"Server returned: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"Connection failed: {e}")
        return False