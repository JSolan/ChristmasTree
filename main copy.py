import os
from dotenv import load_dotenv
from app.api import WLEDAPI
from app.control import set_led_colors, apply_effect

# Load environment variables from .env
load_dotenv()

# Get the WLED IP from environment variables
WLED_IP = os.getenv("WLED_IP")

def main():
    if not WLED_IP:
        raise ValueError("WLED_IP is not set in .env file")
    
    api = WLEDAPI(WLED_IP)
    print(f"Connected to WLED at {WLED_IP}")

    # Example: Set colors for first three LEDs
    colors = [
        [255, 0, 0],  # Red
        [0, 255, 0],  # Green
        [0, 0, 255],  # Blue
    ]
    set_led_colors(api, colors)

    # Example: Apply a built-in effect
    apply_effect(api, effect_id=1)  # Rainbow effect

if __name__ == "__main__":
    main()
