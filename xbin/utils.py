import requests

def turn_off_all_leds(api_url, led_count):
    """
    Turns off all LEDs by setting their colors to black.
    :param api_url: The WLED API endpoint.
    :param led_count: The total number of LEDs.
    """
    print("Turning off all LEDs...")
    payload = {
        "seg": [{
            "id": 0,
            "start": 0,
            "stop": led_count,
            "col": [[0, 0, 0]],  # Set all LEDs to black
            "on": True  # Keep the segment active
        }]
    }
    response = requests.post(api_url, json=payload)
    if response.status_code == 200:
        print("All LEDs turned off successfully.")
    else:
        print(f"Failed to turn off LEDs: {response.text}")
