import requests

class WLEDController:
    def __init__(self, ip, led_count):
        """
        Initialize the WLEDController with device IP and LED count.
        :param ip: The IP address of the WLED device.
        :param led_count: Total number of LEDs.
        """
        self.api_url = f"http://{ip}/json/state"
        self.led_count = led_count

    def set_state(self, payload):
        """
        Sends a JSON payload to the WLED API.
        :param payload: The JSON payload for the WLED state.
        """
        try:
            response = requests.post(self.api_url, json=payload)
            if response.status_code == 200:
                print("State updated successfully.")
            else:
                print(f"Failed to update state: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Error during API call: {e}")

    def turn_off_all_leds(self):
        """
        Turns off all LEDs by setting their colors to black.
        """
        print("Turning off all LEDs...")
        payload = {
            "seg": [{
                "id": 0,
                "start": 0,
                "stop": self.led_count,
                "col": [[0, 0, 0]],  # Set all LEDs to black
                "on": True  # Keep the segment active
            }]
        }
        self.set_state(payload)

    def turn_on_single_led(self, led_id, color=(255, 255, 255), brightness=255):
        """
        Turns on a single LED and turns off all others.
        :param led_id: The ID of the LED to turn on.
        :param color: The RGB color tuple for the LED.
        :param brightness: Brightness of the LED (0-255).
        """
        if not (0 <= led_id < self.led_count):
            print(f"Error: LED ID {led_id} is out of range. Must be between 0 and {self.led_count - 1}.")
            return

        print(f"Turning on single LED {led_id}...")
        payload = {
            "seg": [{
                "id": 0,
                "start": led_id,
                "stop": led_id + 1,
                "col": [list(color)],
                "on": True,
                "bri": brightness
            }]
        }
        self.set_state(payload)

    def turn_on_all_leds(self, color=(255, 255, 255), brightness=255):
        """
        Turns on all LEDs with the same color and brightness.
        :param color: The RGB color tuple for the LEDs.
        :param brightness: Brightness of the LEDs (0-255).
        """
        print(f"Turning on all LEDs to color {color} and brightness {brightness}...")
        payload = {
            "seg": [{
                "id": 0,
                "start": 0,
                "stop": self.led_count,
                "col": [list(color)],
                "on": True,
                "bri": brightness
            }]
        }
        self.set_state(payload)
