import cv2

def camera_feed(camera_index=0):
    # Open the camera
    cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)  # Use DirectShow backend for better compatibility

    if not cap.isOpened():
        print("Error: Could not open the camera.")
        return

    print("Press 'q' to exit the video feed.")

    while True:
        # Read a frame from the camera
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame from the camera.")
            break

        # Display the frame
        cv2.imshow("Camera Feed", frame)

        # Break on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    camera_feed()
