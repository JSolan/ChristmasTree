import json
import time
from utils.wled_controller import WLEDController

# Load configuration from config.json
with open("config.json", "r") as config_file:
    config = json.load(config_file)

# Configuration variables
WLED_IP = config["wled_ip"]
LED_COUNT = config["led_count"]
SEQUENCE_WAIT = config["sequence_wait"]  # Delay in seconds between LEDs

def main():
    # Initialize the WLEDController
    controller = WLEDController(WLED_IP, LED_COUNT)

    # Turn off all LEDs
    controller.turn_off_all_leds()

    # Sequentially turn on each LED
    for led_id in range(LED_COUNT):
        controller.turn_on_single_led(led_id=led_id, color=(255, 255, 255), brightness=255)
        time.sleep(SEQUENCE_WAIT)  # Wait before turning on the next LED

    for led_id in reversed(range(LED_COUNT)):
        controller.turn_on_single_led(led_id=led_id, color=(255, 255, 255), brightness=255)
        time.sleep(SEQUENCE_WAIT)

    for led_id in range(LED_COUNT):
        controller.turn_on_single_led(led_id=led_id, color=(255, 255, 255), brightness=255)
        time.sleep(SEQUENCE_WAIT)

    # Turn off all LEDs at the end of the sequence
    controller.turn_off_all_leds()

if __name__ == "__main__":
    main()
