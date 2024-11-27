import json
import os
import matplotlib.pyplot as plt

def main():
    # Path to the 2d_map.json file
    data_file = os.path.join("data", "2d_map.json")

    # Check if the file exists
    if not os.path.exists(data_file):
        print(f"Error: {data_file} not found.")
        return

    # Load LED position data
    with open(data_file, "r") as json_file:
        led_positions = json.load(json_file)

    # Extract x, y positions and IDs
    x_coords = []
    y_coords = []
    ids = []

    for led in led_positions:
        if led["position"]:  # Only include LEDs with valid positions
            x, y = led["position"]
            x_coords.append(x)
            y_coords.append(y)
            ids.append(led["id"])

    # Check if there are valid positions to plot
    if not x_coords or not y_coords:
        print("Error: No valid LED positions found in the data.")
        return

    # Create a scatter plot
    plt.figure(figsize=(10, 8))
    plt.scatter(x_coords, y_coords, c='blue', s=50, label='LED Positions', alpha=0.7)

    # Annotate each point with its ID
    for i, txt in enumerate(ids):
        plt.annotate(txt, (x_coords[i], y_coords[i]), fontsize=9, ha='right')

    # Set plot labels and title
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.title("2D LED Position Map")
    plt.gca().invert_yaxis()  # Invert y-axis to match image coordinates
    plt.legend()
    plt.grid(True)

    # Show the plot
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
