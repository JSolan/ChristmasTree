import time
from dotenv import load_dotenv
import os
from app.api import WLEDAPI

# Load environment variables
load_dotenv()
WLED_IP = os.getenv("WLED_IP")
LED_COUNT = int(os.getenv("LED_COUNT", 50))  # Default to 50 LEDs

if not WLED_IP:
    raise ValueError("WLED_IP is not set in the .env file")


def turn_off_all_leds(api):
    """
    Turn off all LEDs by setting their colors to black.
    :param api: WLED API instance.
    """
    print("Turning off all LEDs...")
    api.set_state({
        "seg": [{
            "id": 0,
            "start": 0,
            "stop": LED_COUNT,
            "col": [[0, 0, 0]],  # Set all LEDs to black
            "on": True  # Keep the segment active
        }]
    })


def highlight_led(api, led_id):
    """
    Highlight a specific LED by turning it on while turning off all others.
    :param api: WLED API instance.
    :param led_id: The ID of the LED to highlight.
    """
    if not (0 <= led_id < LED_COUNT):
        print(f"Error: LED ID {led_id} is out of range. Must be between 0 and {LED_COUNT - 1}.")
        return

    print(f"Highlighting LED {led_id}...")
    api.set_state({
        "seg": [{
            "id": 0,
            "start": led_id,
            "stop": led_id + 1,
            "col": [[255, 255, 255]],  # Set the LED to white
            "on": True
        }]
    })


if __name__ == "__main__":
    # Initialize the WLED API
    api = WLEDAPI(WLED_IP)

    # Turn off all LEDs
    turn_off_all_leds(api)
    time.sleep(1)  # Wait for all LEDs to turn off

    # Get the LED ID to highlight
    try:
        led_id = int(input(f"Enter the LED ID to highlight (0 to {LED_COUNT - 1}): ").strip())
        highlight_led(api, led_id)
    except ValueError:
        print("Invalid input. Please enter a number.")
25
