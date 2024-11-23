import json
import time
from dotenv import load_dotenv
import os
from app.api import WLEDAPI

# Load environment variables
load_dotenv()
WLED_IP = os.getenv("WLED_IP")
if not WLED_IP:
    raise ValueError("WLED_IP is not set in the .env file")

# Load the LED map
LED_MAP_FILE = "led_map_3d_pixels.json"
with open(LED_MAP_FILE, "r") as f:
    led_positions = json.load(f)

# Sort LEDs by height (y-coordinate)
sorted_leds = sorted(led_positions.values(), key=lambda led: led["position"][1])  # Sort by y-coordinate

# Wave effect parameters
MAX_BRIGHTNESS = 255  # Maximum brightness
DELAY_SECONDS = 0.1   # Delay between steps
Y_THRESHOLD = 20      # Threshold for grouping LEDs by proximity in the y-axis


def calculate_brightness(led_y, wave_y, max_brightness, y_threshold):
    """
    Calculate the brightness of an LED based on its proximity to the wave's y-coordinate.
    :param led_y: The y-coordinate of the LED.
    :param wave_y: The current y-coordinate of the wave.
    :param max_brightness: The maximum brightness level.
    :param y_threshold: The threshold for determining proximity.
    :return: Brightness level (0 to max_brightness).
    """
    distance = abs(led_y - wave_y)
    if distance > y_threshold:
        return 0  # Completely out of range
    return int(max_brightness * (1 - (distance / y_threshold)))  # Scale brightness


def wave_effect(api, sorted_leds, max_brightness, delay_seconds, y_threshold):
    """
    Create a wave effect where LEDs brighten and dim based on proximity in the y-axis.
    :param api: WLEDAPI instance.
    :param sorted_leds: List of LEDs sorted by y-coordinate.
    :param max_brightness: Maximum brightness for the wave.
    :param delay_seconds: Delay between steps in the wave.
    :param y_threshold: Threshold for grouping LEDs by proximity in the y-axis.
    """
    print("Starting wave effect...")

    # Get the range of y values
    min_y = min(led["position"][1] for led in sorted_leds)
    max_y = max(led["position"][1] for led in sorted_leds)

    # Run the wave
    for wave_y in range(int(min_y), int(max_y) + 1, y_threshold):
        # Prepare the state for all LEDs
        led_segments = []
        for led in sorted_leds:
            led_id = led["id"]
            brightness = calculate_brightness(led["position"][1], wave_y, max_brightness, y_threshold)
            if brightness > 0:
                led_segments.append({
                    "id": 0,
                    "start": led_id,
                    "stop": led_id + 1,
                    "col": [[brightness, brightness, brightness]],  # Set LED color to white with calculated brightness
                    "on": True
                })

        # Send state to WLED
        if led_segments:
            api.set_state({"seg": led_segments})

        time.sleep(delay_seconds)

    print("Wave effect completed.")


if __name__ == "__main__":
    # Initialize the WLED API
    api = WLEDAPI(WLED_IP)

    # Run the wave effect
    wave_effect(api, sorted_leds, MAX_BRIGHTNESS, DELAY_SECONDS, Y_THRESHOLD)
