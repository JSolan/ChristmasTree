import cv2
import json
import time
from dotenv import load_dotenv
import os
from app.api import WLEDAPI

# Load environment variables
load_dotenv()
WLED_IP = os.getenv("WLED_IP").strip()
LED_COUNT = int(os.getenv("LED_COUNT", 100))  # Default to 50 LEDs
DELAY_PER_LED = 0.5  # Delay in seconds for each LED capture

if not WLED_IP:
    raise ValueError("WLED_IP is not set in the .env file")


def turn_off_all_leds(api):
    """
    Set all LEDs to 'off' (dark state) by setting their colors to black.
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


def capture_led_positions(api, camera, led_count, position_name):
    """
    Capture the 2D positions of LEDs from a single camera position.
    :param api: WLED API instance.
    :param camera: OpenCV VideoCapture instance.
    :param led_count: Number of LEDs.
    :param position_name: Name of the camera position (e.g., 'Position 1').
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
        time.sleep(DELAY_PER_LED)
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


def calculate_3d_positions(all_positions):
    """
    Calculate the 3D positions of LEDs based on multiple camera positions.
    :param all_positions: List of 2D positions from multiple camera positions.
    :return: Dictionary of 3D positions.
    """
    if len(all_positions) < 2:
        print("Error: At least two camera positions are required for 3D mapping.")
        return {}

    led_positions_3d = {}

    for i in range(len(all_positions[0])):  # Assuming all positions captured the same number of LEDs
        x_values, y_values, disparities = [], [], []

        for p1, p2 in zip(all_positions[:-1], all_positions[1:]):
            if p1[i] and p2[i]:
                x_values.append(p1[i][0])
                y_values.append(p1[i][1])
                disparity = abs(p1[i][0] - p2[i][0])
                if disparity > 0:
                    disparities.append(disparity)

        if x_values and y_values and disparities:
            avg_x = sum(x_values) / len(x_values)
            avg_y = sum(y_values) / len(y_values)
            avg_disparity = sum(disparities) / len(disparities)
            z = 1 / avg_disparity  # Simplified depth calculation
            led_positions_3d[f"led_{i}"] = {"id": i, "position": [avg_x, avg_y, z]}
            print(f"LED {i}: (x, y, z) = ({avg_x:.2f}, {avg_y:.2f}, {z:.2f})")
        else:
            print(f"LED {i} not detected in all positions. Skipping.")

    return led_positions_3d


if __name__ == "__main__":
    api = WLEDAPI(WLED_IP)
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("Error: Could not open the camera.")
        exit()

    turn_off_all_leds(api)

    all_positions = []
    position_counter = 1

    while True:
        print(f"\nPosition the camera for Position {position_counter} and press Enter to show the camera feed.")
        input("Press Enter to continue...")
        
        print("Starting camera feed. Press 'q' to exit the feed and start capturing.")
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read from camera.")
                break
            cv2.imshow(f"Camera Feed - Position {position_counter}", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()
        print(f"Starting capture for Position {position_counter}...")
        positions = capture_led_positions(api, cap, LED_COUNT, f"Position {position_counter}")
        all_positions.append(positions)

        another_position = input("\nDo you want to capture another camera position? (yes/no): ").strip().lower()
        if another_position == "yes":
            # Turn all LEDs to dark before the next capture
            turn_off_all_leds(api)
            position_counter += 1
        else:
            break

    print("Calculating 3D positions...")
    led_positions_3d = calculate_3d_positions(all_positions)

    output_file = "led_map_3d.json"
    with open(output_file, "w") as f:
        json.dump(led_positions_3d, f, indent=4)
    print(f"3D LED positions saved to {output_file}.")

    cap.release()
    cv2.destroyAllWindows()
