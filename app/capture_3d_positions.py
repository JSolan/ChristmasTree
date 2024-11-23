import cv2
import json
import os
import time  # Import time for adding delay
from dotenv import load_dotenv
from app.api import WLEDAPI

# Load environment variables
load_dotenv()
WLED_IP = os.getenv("WLED_IP")
LED_COUNT = int(os.getenv("LED_COUNT", 50))  # Default to 50 LEDs
BASELINE_PIXELS = 50  # Baseline in pixels (adjust as needed)
DELAY_SECONDS = 0.5  # Delay between setting an LED and capturing (adjust as needed)

if not WLED_IP:
    raise ValueError("WLED_IP is not set in the .env file")


def turn_off_all_leds(api, led_count):
    """
    Set all LEDs to 'off' (dark state) by setting their colors to black.
    :param api: WLED API instance.
    :param led_count: Total number of LEDs in the strip.
    """
    print("Setting all LEDs to dark...")
    api.set_state({
        "seg": [{
            "id": 0,  # Default segment
            "start": 0,
            "stop": led_count,
            "col": [[0, 0, 0]],  # Set all LEDs to black
            "on": True  # Keep the segment active
        }]
    })


def detect_led(frame):
    """
    Detect the LED position in the frame.
    :param frame: Captured frame from the camera.
    :return: Tuple (x, y) of LED center, or None if not found.
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        return x + w // 2, y + h // 2  # Center of the LED

    return None


def capture_led_positions(api, camera, led_count, position_name, delay_seconds=DELAY_SECONDS):
    """
    Capture the 2D positions of LEDs from a single camera position.
    :param api: WLED API instance.
    :param camera: OpenCV VideoCapture instance.
    :param led_count: Number of LEDs.
    :param position_name: Name of the camera position (e.g., 'Position 1').
    :param delay_seconds: Delay between LED activation and capture.
    :return: List of (x, y) coordinates for each LED.
    """
    print(f"Capturing LEDs from {position_name}...")
    positions = []

    for i in range(led_count):
        print(f"Capturing LED {i}...")
        api.set_state({
            "seg": [{
                "id": 0,
                "start": i,
                "stop": i + 1,
                "col": [[255, 255, 255]],  # Set the LED to white for detection
                "on": True
            }]
        })
        time.sleep(delay_seconds)  # Wait for the LED to stabilize
        ret, frame = camera.read()

        if not ret:
            print(f"Error: Could not capture frame for LED {i}.")
            positions.append(None)
            continue

        led_position = detect_led(frame)
        if led_position:
            print(f"LED {i} detected at {led_position}.")
        else:
            print(f"LED {i} not detected.")
        positions.append(led_position)

    return positions


def calculate_3d_positions(positions1, positions2, baseline_pixels):
    """
    Calculate the 3D positions of LEDs based on two camera positions.
    :param positions1: List of 2D positions from position 1.
    :param positions2: List of 2D positions from position 2.
    :param baseline_pixels: Baseline distance in pixels.
    :return: Dictionary of 3D positions.
    """
    led_positions_3d = {}

    for i, (led1, led2) in enumerate(zip(positions1, positions2)):
        if led1 and led2:
            disparity = abs(led1[0] - led2[0])  # Difference in x-coordinates
            if disparity > 0:
                z_pixels = baseline_pixels / disparity  # Relative depth (larger disparity = closer LED)
                x_pixels = led1[0]  # Use x from the first camera position
                y_pixels = led1[1]  # Use y from the first camera position
                led_positions_3d[f"led_{i}"] = {"id": i, "position": [x_pixels, y_pixels, z_pixels]}
                print(f"LED {i}: (x, y, z) = ({x_pixels:.2f}, {y_pixels:.2f}, {z_pixels:.2f}) pixels")
            else:
                print(f"Disparity for LED {i} is too small. Skipping.")
        else:
            print(f"LED {i} not detected in both positions. Skipping.")

    return led_positions_3d


if __name__ == "__main__":
    api = WLEDAPI(WLED_IP)

    # Turn off all LEDs before starting the script
    turn_off_all_leds(api, LED_COUNT)

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("Error: Could not open the camera.")
        exit()

    # Capture positions from Camera Position 1
    input("Position the camera at the first position and press Enter to continue...")
    positions1 = capture_led_positions(api, cap, LED_COUNT, "Position 1")

    # Signal to move the camera
    print("Capture from Position 1 complete. Move the camera to Position 2.")
    input("Position the camera at the second position and press Enter to continue...")

    # Capture positions from Camera Position 2
    positions2 = capture_led_positions(api, cap, LED_COUNT, "Position 2")

    # Calculate 3D positions
    print("Calculating 3D positions...")
    led_positions_3d = calculate_3d_positions(positions1, positions2, BASELINE_PIXELS)

    # Save 3D positions to JSON file
    output_file = "led_map_3d_pixels.json"
    with open(output_file, "w") as f:
        json.dump(led_positions_3d, f, indent=4)
    print(f"3D LED positions saved to {output_file}.")

    cap.release()
    cv2.destroyAllWindows()
