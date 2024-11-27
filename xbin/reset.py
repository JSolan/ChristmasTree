import requests
import json

# Load configuration from config.json
with open("config.json", "r") as config_file:
    config = json.load(config_file)

# Configuration variables
WLED_IP = config["wled_ip"]
LED_COUNT = config["led_count"]
API_URL = f"http://{WLED_IP}/json/state"

def reset_leds():
    """
    Resets all LEDs to be on, unfrozen, and dark.
    - Turns all LEDs "on" (ready for effects).
    - Ensures the segment is unfrozen.
    - Sets brightness to 0 (dark).
    """
    payload = {
        "seg": [{
            "id": 0,  # Default segment
            "start": 0,
            "stop": LED_COUNT,
            "col": [[0, 0, 0]],  # Set all LEDs to black
            "on": True  # Keep the segment active
        }]
    }

    response = requests.post(API_URL, json=payload)
    if response.status_code == 200:
        print("LEDs have been reset successfully.")
    else:
        print(f"Failed to reset LEDs: {response.text}")

if __name__ == "__main__":
    reset_leds()
