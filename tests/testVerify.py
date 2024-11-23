import requests

# Replace with your WLED IP
WLED_IP = "10.128.150.10"

# Fetch current state
response = requests.get(f"http://{WLED_IP}/json")
if response.status_code == 200:
    print("Connected to WLED!")
    print("Device State:", response.json())
else:
    print(f"Failed to connect: {response.status_code}")
