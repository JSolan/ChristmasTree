import cv2
import json
import os
from dotenv import load_dotenv
from app.api import WLEDAPI

# Load environment variables
load_dotenv()
WLED_IP = os.getenv("WLED_IP")

if not WLED_IP:
    raise ValueError("WLED_IP is not set in the .env file")

def capture_led_positions(api, camera_index=0, led_count=50, output_file="led_map.json"):
    """
    Capture the positions of LEDs using a camera and save them to a file.
    :param api: Instance of WLEDAPI.
    :param camera_index: Camera index for OpenCV.
    :param led_count: Total number of LEDs.
    :param output_file: JSON file to save the LED positions.
    """
    # Open the camera
    cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if not cap.isOpened():
        print("Error: Could not open the camera.")
        return

    print("Press 'q' to stop the process manually.")

    led_map = {}

    for i in range(led_count):
        print(f"Capturing position for LED {i}...")

        # Turn on a single LED
        api.set_state({"seg": [{"id": 0, "start": i, "stop": i + 1, "on": True}]})

        # Capture an image
        ret, frame = cap.read()
        if not ret:
            print(f"Error: Could not capture frame for LED {i}.")
            continue

        # Convert to grayscale and threshold
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)  # Adjust threshold if needed

        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Find the largest contour (assuming it's the LED)
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            led_map[f"led_{i}"] = {
                "id": i,
                "position": [x + w // 2, -(y + h // 2)]  # y inverted here
            }

            # Draw a rectangle for visualization
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Display the frame for debugging
        cv2.imshow("LED Mapping", frame)

        # Press 'q' to quit
        if cv2.waitKey(500) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

    # Save LED positions to a JSON file
    with open(output_file, "w") as f:
        json.dump(led_map, f, indent=4)
    print(f"LED positions saved to {output_file}.")


if __name__ == "__main__":
    # Create the WLED API instance
    api = WLEDAPI(WLED_IP)
    capture_led_positions(api)
