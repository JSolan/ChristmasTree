import json
from utils.wled_controller import WLEDController

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

    # Prompt the user for the LED ID
    try:
        led_id = int(input(f"Enter the LED ID to highlight (0 to {LED_COUNT - 1}): ").strip())
        
        # Check if the input is within range
        if 0 <= led_id < LED_COUNT:
            # Highlight the specified LED
            controller.turn_on_single_led(led_id=led_id, color=(255, 255, 255), brightness=255)
        else:
            print(f"Error: LED ID {led_id} is out of range. Must be between 0 and {LED_COUNT - 1}.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")

if __name__ == "__main__":
    main()
