import cv2

class CameraFeed:
    def __init__(self, camera_index=0):
        """
        Initializes the CameraFeed class.
        :param camera_index: The index of the camera to use (default is 0 for the first camera).
        """
        self.camera_index = camera_index
        self.cap = None

    def initialize_camera(self):
        """
        Initializes the camera using the DirectShow backend for faster startup.
        """
        print(f"Initializing camera at index {self.camera_index}...")
        self.cap = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW)  # Use DirectShow for faster initialization
        if not self.cap.isOpened():
            raise RuntimeError(f"Error: Could not open the camera (index {self.camera_index}).")
        print(f"Camera initialized successfully (index {self.camera_index}).")

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
