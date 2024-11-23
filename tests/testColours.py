import requests

WLED_IP = "10.128.150.10"  # Replace with your WLED IP
API_URL = f"http://{WLED_IP}/json/state"

# Set colors for the first three LEDs
payload = {
    "seg": [
        {
            "i": [
                [255, 0, 0],  # LED 1 red
                [0, 255, 0],  # LED 2 green
                [0, 0, 255]   # LED 3 blue
            ]
        }
    ]
}

response = requests.post(API_URL, json=payload)
if response.status_code == 200:
    print("LED colors updated!")
else:
    print(f"Failed to update LEDs: {response.status_code} {response.text}")
