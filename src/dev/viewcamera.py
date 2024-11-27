from src.utils.camera_controller import CameraFeed

def main():
    # Initialize the camera feed
    camera_feed = CameraFeed(camera_index=0)
    
    try:
        # Initialize the camera
        camera_feed.initialize_camera()
        camera_feed.set_camera_parameters(resolution=(1280, 720), exposure=-5)
        camera_feed.set_rotation(0)
        # Show the camera feed
        camera_feed.show_camera_feed(window_name="Camera Feed")
    except RuntimeError as e:
        print(e)
    finally:
        # Ensure the camera is closed properly
        camera_feed.close_camera()

if __name__ == "__main__":
    main()