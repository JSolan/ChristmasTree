import cv2
import numpy as np


class CameraFeed:
    def __init__(self, camera_index=0):
        """
        Initializes the CameraFeed class.
        :param camera_index: The index of the camera to use (default is 0 for the first camera).
        """
        self.camera_index = camera_index
        self.cap = None
        self.rotation = 0  # Default rotation: 0 degrees
        self.mirror = False  # Default: No mirroring

    def initialize_camera(self):
        """
        Initializes the camera using the DirectShow backend for faster startup.
        """
        print(f"Initializing camera at index {self.camera_index}...")
        self.cap = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW)  # Use DirectShow for faster initialization
        if not self.cap.isOpened():
            raise RuntimeError(f"Error: Could not open the camera (index {self.camera_index}).")
        print(f"Camera initialized successfully (index {self.camera_index}).")

    def set_camera_parameters(self, resolution=(1920, 1080), exposure=-7):
        """
        Sets the camera parameters.
        :param resolution: Tuple (width, height) for the camera resolution.
        :param exposure: Exposure value (lower for darker images).
        """
        if not self.cap:
            raise RuntimeError("Error: Camera not initialized. Call `initialize_camera()` first.")

        print(f"Setting camera resolution to {resolution} and exposure to {exposure}...")
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])
        self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)  # Manual mode
        self.cap.set(cv2.CAP_PROP_EXPOSURE, exposure)
        print("Camera parameters set.")

    def set_rotation(self, rotation: int):
        """
        Sets the rotation mode for the camera feed.
        :param rotation: Rotation angle (0, 90, 180, 270 degrees clockwise).
        """
        if rotation not in [0, 90, 180, 270]:
            raise ValueError("Invalid rotation angle. Use 0, 90, 180, or 270.")
        self.rotation = rotation
        print(f"Camera feed rotation set to: {rotation} degrees")

    def set_mirror(self, mirror: bool):
        """
        Sets the mirroring mode for the camera feed.
        :param mirror: True to mirror the feed, False to keep it normal.
        """
        self.mirror = mirror
        print(f"Camera feed mirroring set to: {'Enabled' if mirror else 'Disabled'}")

    def apply_transformations(self, frame):
        """
        Applies rotation and mirroring transformations to the frame.
        :param frame: Input frame from the camera.
        :return: Transformed frame.
        """
        if self.rotation == 90:
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        elif self.rotation == 180:
            frame = cv2.rotate(frame, cv2.ROTATE_180)
        elif self.rotation == 270:
            frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

        if self.mirror:
            frame = cv2.flip(frame, 1)  # Horizontal flip for mirroring

        return frame

    def show_camera_feed(self, window_name="Camera Feed"):
        """
        Opens the camera feed and displays it in a window. The feed will close when the user presses 'q'.
        """
        if not self.cap:
            raise RuntimeError("Error: Camera not initialized. Call `initialize_camera()` first.")

        print("Starting camera feed. Press 'q' to close.")
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Could not read from the camera.")
                break

            # Apply transformations
            frame = self.apply_transformations(frame)

            cv2.imshow(window_name, frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Closing camera feed...")
                break

        self.close_camera()

    def close_camera(self):
        """
        Releases the camera and closes any OpenCV windows.
        """
        if self.cap and self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()
        print("Camera feed closed.")


import cv2

class BrightSpot:
    def __init__(self, threshold=200, min_contour_area=50):
        """
        Initializes the BrightSpot class.
        :param threshold: Brightness threshold for detecting bright spots (0-255).
        :param min_contour_area: Minimum contour area to filter out noise.
        """
        self.threshold = threshold
        self.min_contour_area = min_contour_area

    def find_bright_spot(self, frame):
        """
        Finds the brightest spot in a given frame.
        :param frame: The frame to process (numpy array).
        :return: (x, y) coordinates of the brightest spot, or None if no spot is found.
        """
        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply a threshold to isolate bright areas
        _, thresh = cv2.threshold(gray, self.threshold, 255, cv2.THRESH_BINARY)

        # Find contours of the bright areas
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            return None  # No bright spots found

        # Filter contours by area
        contours = [c for c in contours if cv2.contourArea(c) >= self.min_contour_area]
        if not contours:
            return None  # No valid contours remain

        # Find the largest bright spot
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)

        # Calculate centroid for higher precision
        moments = cv2.moments(largest_contour)
        if moments["m00"] != 0:
            # cx, cy = x + w // 2, y + h // 2
            cx = int(moments["m10"] / moments["m00"])
            cy = int(moments["m01"] / moments["m00"])
        else:
            # Fallback to bounding box center
            cx, cy = x + w // 2, y + h // 2

        return cx, cy
