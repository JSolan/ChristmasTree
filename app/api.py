import requests

class WLEDAPI:
    def __init__(self, ip):
        self.base_url = f"http://{ip}/json"

    def set_state(self, payload):
        """
        Sends a state update to the WLED device.
        :param payload: JSON payload to set LED state.
        """
        url = f"{self.base_url}/state"
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise error for bad requests
        return response.json()

    def get_state(self):
        """
        Fetches the current state of the WLED device.
        """
        response = requests.get(self.base_url)
        response.raise_for_status()
        return response.json()
