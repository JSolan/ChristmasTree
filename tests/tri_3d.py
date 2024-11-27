from app.api import WLEDAPI
from dev_tools.camera_utils import LEDCapture
import cv2
import json
import numpy as np
import time

# Configuration
CAMERA_INTRINSICS = np.array([[1200, 0, 960], [0, 1200, 540], [0, 0, 1]])
OUTPUT_FILE = "led_positions_3d_live.json"
LED_COUNT = 100
SEQUENCING_DELAY = 0.2

def perform_led_sequencing(api, led_capture):
    reference_positions = []
    print("Starting LED sequencing...")

    for i in range(LED_COUNT):
        print(f"Sequencing LED {i}...")
        api.set_state({"seg": [{"id": 0, "start": i, "stop": i + 1, "on": True}]})
        time.sleep(SEQUENCING_DELAY)

        # Capture the frame and detect the LED
        frame = led_capture.get_frame()
        led_position = led_capture.detect_leds(frame)
        if led_position:
            print(f"LED {i} detected at {led_position}.")
            reference_positions.append({"id": i, "position": led_position[0]})  # Get the first detected LED
        else:
            print(f"LED {i} not detected.")
            reference_positions.append({"id": i, "position": None})

        api.set_state({"seg": [{"id": 0, "start": i, "stop": i + 1, "on": False}]})

    # Save the reference positions
    with open("led_reference.json", "w") as f:
        json.dump(reference_positions, f, indent=4)
    print("LED sequencing complete. Reference positions saved.")
    return reference_positions

def main():
    api = WLEDAPI("10.128.150.10")  # Replace with your WLED IP
    led_capture = LEDCapture(camera_index=0)

    try:
        # Perform LED sequencing
        reference_positions = perform_led_sequencing(api, led_capture)

        print("Starting live capture. Move the camera around LEDs and press 'q' to stop.")
        frames = []
        led_positions = []

        while True:
            frame = led_capture.get_frame()
            cv2.imshow("Camera Feed", frame)

            # Detect LEDs in the frame
            positions = led_capture.detect_leds(frame)
            led_positions.append(positions)

            # Add frame to list
            frames.append(frame)

            # Stop recording on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        print(f"Captured {len(frames)} frames.")
        
        # (Further processing and triangulation can follow here)

    finally:
        led_capture.release()


if __name__ == "__main__":
    main()
