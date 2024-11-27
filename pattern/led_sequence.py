import time
from dotenv import load_dotenv
import os
from app.api import WLEDAPI

# Load environment variables
load_dotenv()
WLED_IP = os.getenv("WLED_IP")
LED_COUNT = int(os.getenv("LED_COUNT", 50))  # Default to 50 LEDs
LED_ON_TIME = float(os.getenv("LED_ON_TIME", 50))   # Default LED on time (in seconds)

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


def light_up_leds_in_sequence(api, led_count, on_time):
    """
    Turn on each LED in sequence for a specified duration.
    :param api: WLED API instance.
    :param led_count: Total number of LEDs.
    :param on_time: Time (in seconds) each LED should remain on.
    """
    print("Lighting up LEDs in sequence...")
    for led_id in range(led_count):
        print(f"Lighting up LED {led_id}...")
        api.set_state({
            "seg": [{
                "id": 0,
                "start": led_id,
                "stop": led_id + 1,
                "col": [[255, 255, 255]],  # Set LED to white
                "on": True
            }]
        })
        time.sleep(on_time)  # Keep LED on for the specified duration
        # Turn off the current LED before lighting the next one
        api.set_state({
            "seg": [{
                "id": 0,
                "start": led_id,
                "stop": led_id + 1,
                "col": [[0, 0, 0]],  # Set LED back to black
                "on": True
            }]
        })


if __name__ == "__main__":
    # Initialize the WLED API
    api = WLEDAPI(WLED_IP)

    # Turn off all LEDs initially
    turn_off_all_leds(api)
    time.sleep(1)  # Small delay to ensure all LEDs are off

    # Light up LEDs in sequence
    light_up_leds_in_sequence(api, LED_COUNT, LED_ON_TIME)

    print("LED sequence complete.")
