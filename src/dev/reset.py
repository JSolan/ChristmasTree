import json
from src.utils.wled_controller import WLEDController

# Load configuration from config.json
with open("config.json", "r") as config_file:
    config = json.load(config_file)

# Configuration variables
WLED_IP = config["wled_ip"]
LED_COUNT = config["led_count"]

def main():
    # Initialize the WLEDController
    controller = WLEDController(WLED_IP, LED_COUNT)

    # Turn off all LEDs
    controller.turn_off_all_leds()

if __name__ == "__main__":
    main()
