import requests

# Replace with your WLED IP
WLED_IP = "10.128.150.10"
API_URL = f"http://{WLED_IP}/json/state"

def reset_segment_and_apply_effect(effect_id, palette_id=0, led_count=50):
    """
    Reset WLED segment configuration and apply an effect.
    :param effect_id: WLED effect ID to apply.
    :param palette_id: WLED palette ID to apply.
    :param led_count: Total number of LEDs in the strip.
    """
    payload = {
        "on": True,  # Ensure LEDs are powered on
        "seg": [
            {
                "id": 0,         # Segment ID
                "start": 0,      # Start of segment
                "stop": led_count,  # End of segment
                "fx": effect_id,  # Effect ID
                "pal": palette_id,  # Palette ID
                "frz": False,    # Unfreeze the segment
                "bri": 255       # Maximum brightness
            }
        ]
    }

    print(f"Sending payload to {API_URL}: {payload}")
    response = requests.post(API_URL, json=payload)

    if response.status_code == 200:
        print("Successfully applied effect and updated segment!")
        print("Response from WLED:", response.json())
    else:
        print(f"Failed to apply effect: {response.status_code} - {response.text}")

if __name__ == "__main__":
    print("WLED Effect Tester with Segment Reset")
    print("Enter an effect ID to test (e.g., 9 for Rainbow).")
    print("You can find effect IDs in the WLED documentation.")
    
    try:
        effect_id = int(input("Enter effect ID: "))
        palette_id = int(input("Enter palette ID (default is 0): ") or 0)
        led_count = int(input("Enter the total number of LEDs (default is 50): ") or 50)

        # Reset the segment and apply the effect
        reset_segment_and_apply_effect(effect_id, palette_id, led_count)

    except ValueError:
        print("Invalid input. Please enter valid numbers for effect, palette, and LED count.")
    except Exception as e:
        print(f"An error occurred: {e}")
