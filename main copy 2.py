import os
from dotenv import load_dotenv
from app.api import WLEDAPI

def reset_segment_and_apply_effect(api, effect_id, palette_id=0, led_count=50):
    """
    Reset WLED segment configuration and apply an effect.
    :param api: Instance of WLEDAPI.
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

    print(f"Sending payload: {payload}")
    response = api.set_state(payload)

    if response:
        print("Successfully applied effect and updated segment!")
    else:
        print("Failed to apply effect.")

def main():
    # Load .env variables
    load_dotenv()
    WLED_IP = os.getenv("WLED_IP")

    if not WLED_IP:
        raise ValueError("WLED_IP is not set in .env file")

    # Initialize API
    api = WLEDAPI(WLED_IP)
    print(f"Connected to WLED at {WLED_IP}")

    # Input effect and palette from the user
    try:
        effect_id = int(input("Enter effect ID (e.g., 9 for Rainbow): "))
        palette_id = int(input("Enter palette ID (default is 0): ") or 0)
        led_count = int(input("Enter the total number of LEDs (default is 50): ") or 50)

        # Apply effect with segment reset
        reset_segment_and_apply_effect(api, effect_id, palette_id, led_count)

    except ValueError:
        print("Invalid input. Please enter valid numbers for effect, palette, and LED count.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
