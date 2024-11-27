import json
import matplotlib.pyplot as plt

def visualize_led_map(json_file):
    with open(json_file, "r") as f:
        led_positions = json.load(f)

    # Extract x and y coordinates

    x_coords = [data["position"][0] for data in led_positions.values()]
    y_coords = [data["position"][1] for data in led_positions.values()]
    ids = [data["id"] for data in led_positions.values()]

    # Plot the positions
    plt.figure(figsize=(8, 6))
    plt.scatter(x_coords, y_coords, c="blue", label="LEDs")
    plt.title("LED Mapping Visualization")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.legend()
    plt.grid(True)

    # Annotate each point with its ID
    for i, led_id in enumerate(ids):
        plt.text(x_coords[i], y_coords[i], f"ID: {led_id}", fontsize=8, ha='right', va='bottom')

    plt.show()

if __name__ == "__main__":
    visualize_led_map("led_map_3d.json")
