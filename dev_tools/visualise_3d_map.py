import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

def visualize_led_map(json_file):
    with open(json_file, "r") as f:
        led_positions = json.load(f)

    # Extract x, y, z coordinates
    x_coords = [data["position"][0] for data in led_positions.values()]
    y_coords = [data["position"][1] for data in led_positions.values()]
    z_coords = [data["position"][2] for data in led_positions.values()]
    ids = [data["id"] for data in led_positions.values()]

    # Create a 3D scatter plot
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x_coords, y_coords, z_coords, c='blue', marker='o', label="LEDs")

    # Annotate each point with its ID
    for i, led_id in enumerate(ids):
        ax.text(x_coords[i], y_coords[i], z_coords[i], f"ID: {led_id}", fontsize=8)

    # Set labels
    ax.set_title("3D LED Map Visualization")
    ax.set_xlabel("X (mm)")
    ax.set_ylabel("Y (mm)")
    ax.set_zlabel("Z (mm)")
    ax.legend()

    # Show the plot
    plt.show()

if __name__ == "__main__":
    visualize_led_map("led_map_3d.json")
