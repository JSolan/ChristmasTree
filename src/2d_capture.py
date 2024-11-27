import json
import os
import cv2
from utils.wled_controller import WLEDController
from utils.camera_controller import CameraFeed, BrightSpot


def main():
    # Load configuration
    with open("config.json", "r") as config_file:
        config = json.load(config_file)

    WLED_IP = config["wled_ip"]
    LED_COUNT = config["led_count"]
    THRESHOLD = config.get("threshold", 200)  # Default threshold for bright spot detection
    MIN_CONTOUR_AREA = config.get("min_contour_area", 50)  # Default minimum contour area
    PREVIEW_WINDOW_NAME = "Camera Preview"
    OUTPUT_FOLDER = "data"
    XRES = config.get("xres", 1920)
    YRES = config.get("yres", 1080)
    EXPOSURE = config.get("exposure", -7)

    # Initialize components
    wled = WLEDController(WLED_IP, LED_COUNT)
    camera = CameraFeed(camera_index=0)
    detector = BrightSpot(threshold=THRESHOLD, min_contour_area=MIN_CONTOUR_AREA)

    # Initialize camera
    camera.initialize_camera()
    camera.set_camera_parameters(resolution=(XRES, YRES), exposure=EXPOSURE)

    # Allow the user to preview the camera feed before starting
    print("Previewing camera feed. Press 's' to start LED capture or 'q' to quit.")
    while True:
        ret, frame = camera.cap.read()
        if not ret:
            print("Error: Could not read from the camera.")
            break

        frame = camera.apply_transformations(frame)
        cv2.imshow(PREVIEW_WINDOW_NAME, frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):  # Start LED capture
            print("Starting LED capture...")
            break
        elif key == ord('q'):  # Quit
            print("Exiting...")
            camera.close_camera()
            return

    # Create output folder if it doesn't exist
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    output_file = os.path.join(OUTPUT_FOLDER, "2d_map.json")

    led_positions = []  # List to store LED position data

    # Close preview and turn off all LEDs to start
    wled.turn_off_all_leds()

    print("Capturing LED positions...")
    for led_id in range(LED_COUNT):
        # Turn on a single LED
        wled.turn_on_single_led(led_id=led_id, color=(255, 255, 255), brightness=255)
        # Wait for the LED to stabilize
        cv2.waitKey(250)

        # Capture frame from camera
        ret, frame = camera.cap.read()
        if not ret:
            print(f"Error: Could not capture frame for LED {led_id}.")
            led_positions.append({"id": led_id, "position": None})
            continue

        # Apply transformations and detect the bright spot
        frame = camera.apply_transformations(frame)
        bright_spot = detector.find_bright_spot(frame)
        if bright_spot:
            x, y = bright_spot
            print(f"LED {led_id}: Bright spot found at ({x}, {y})")
            led_positions.append({"id": led_id, "position": [x, y]})
        else:
            print(f"LED {led_id}: No bright spot detected.")
            led_positions.append({"id": led_id, "position": None})

    # Save the captured data to JSON
    with open(output_file, "w") as json_file:
        json.dump(led_positions, json_file, indent=4)

    print(f"LED position capture complete. Data saved to {output_file}")

    # Turn off all LEDs and close the camera
    wled.turn_off_all_leds()
    camera.close_camera()


if __name__ == "__main__":
    main()
