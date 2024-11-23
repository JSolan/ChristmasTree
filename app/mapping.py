import cv2
import json
import os
from dotenv import load_dotenv
from app.api import WLEDAPI

# Load .env variables
load_dotenv()
WLED_IP = os.getenv("WLED_IP")

if not WLED_IP:
    raise ValueError("WLED_IP is not set in the .env file")

def capture_led_positions(api, camera_index=0, led_count=50, output_file="led_map.json"):
    """
    Capture LED positions using OpenCV.
    :param api: Instance of WLEDAPI.
    :param camera_index: Index of the camera to use (default is 0).
    :param led_count: Number of LEDs to map.
    :param output_file: File to save the LED positions.
    """
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    led_positions = {}
    for i in range(led_count):
        print(f"Capturing position for LED {i}...")
        
        # Turn on one LED at a time
        api.set_state({"seg": [{"id": 0, "start": i, "stop": i + 1, "on": True}]})
        
        # Capture an image
        ret, frame = cap.read()
        if not ret:
            print(f"Error: Could not capture frame for LED {i}.")
            continue

        # Detect bright spots (e.g., the LED position)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Assume the largest contour is the LED
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            led_positions[f"led_{i}"] = [x + w // 2, y + h // 2]

        # Pause briefly to let the LED stay on
        cv2.imshow("LED Mapping", frame)
        if cv2.waitKey(500) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

    # Save the positions to a file
    with open(output_file, "w") as f:
        json.dump(led_positions, f, indent=4)
    print(f"LED positions saved to {output_file}.")

if __name__ == "__main__":
    # Create the WLEDAPI instance with the IP from .env
    api = WLEDAPI(WLED_IP)
    capture_led_positions(api)
