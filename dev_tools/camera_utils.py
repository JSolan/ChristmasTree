import cv2

class CameraUtils:
    def __init__(self, camera_index=0):
        """
        Initialize the camera utility.
        :param camera_index: Index of the camera to use.
        """
        self.camera_index = camera_index
        self.cap = None

    def initialize_camera(self):
        """
        Open the camera.
        """
        self.cap = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            raise RuntimeError(f"Error: Could not open the camera (index {self.camera_index}).")
        print(f"Camera initialized (index {self.camera_index}).")

    def show_camera_feed(self, window_name="Camera Feed"):
        """
        Display the live camera feed.
        :param window_name: Name of the display window.
        """
        if not self.cap:
            raise RuntimeError("Error: Camera not initialized. Call `initialize_camera()` first.")
        
        print("Starting camera feed. Press 'q' to exit.")
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Could not read from the camera.")
                break
            cv2.imshow(window_name, frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()

    def capture_frame(self):
        """
        Capture a single frame from the camera.
        :return: Captured frame.
        """
        if not self.cap:
            raise RuntimeError("Error: Camera not initialized. Call `initialize_camera()` first.")
        
        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("Error: Could not capture a frame from the camera.")
        return frame

    def detect_led(self, frame):
        """
        Detect the position of the brightest LED in the frame.
        :param frame: Captured frame.
        :return: (x, y) coordinates of the LED center, or None if not found.
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            return x + w // 2, y + h // 2  # Center of the LED

        return None

    def release_camera(self):
        """
        Release the camera resource.
        """
        if self.cap:
            self.cap.release()
            print("Camera released.")
        else:
            print("Warning: Camera was not initialized.")


import cv2
import numpy as np
from typing import List, Tuple


class LEDCapture:
    def __init__(self, camera_index=0, resolution=(1920, 1080), exposure=-7):
        """
        Initialize the LEDCapture class.
        :param camera_index: Index of the camera to use.
        :param resolution: Resolution for the camera feed.
        :param exposure: Camera exposure setting for LED detection.
        """
        self.cap = cv2.VideoCapture(camera_index)
        if not self.cap.isOpened():
            raise ValueError("Error: Could not open the camera.")

        # Set camera properties
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])
        self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)  # Manual mode
        self.cap.set(cv2.CAP_PROP_EXPOSURE, exposure)  # Low exposure for LED detection

    def get_frame(self) -> np.ndarray:
        """
        Capture a single frame from the camera.
        :return: Captured frame.
        """
        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("Error: Could not read frame from the camera.")
        return frame

    def detect_leds(self, frame: np.ndarray) -> List[Tuple[int, int]]:
        """
        Detect LEDs in a single frame.
        :param frame: Input video frame.
        :return: List of (x, y) positions of detected LEDs.
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        leds = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            leds.append((x + w // 2, y + h // 2))  # Center of the LED
        return leds

    def release(self):
        """
        Release the camera resources.
        """
        self.cap.release()
        cv2.destroyAllWindows()
