from utils.camera_controller import CameraFeed

def main():
    camera = CameraFeed(camera_index=0)

    # Initialize the camera
    camera.initialize_camera()

    # Show the camera feed
    camera.show_camera_feed()

if __name__ == "__main__":
    main()
