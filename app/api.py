import requests

class WLEDAPI:
    def __init__(self, ip):
        self.base_url = f"http://{10.128.150.10}/json"

    def set_state(self, payload):
        response = requests.post(f"{self.base_url}/state", json=payload)
        return response.json()

    def get_state(self):
        response = requests.get(self.base_url)
        return response.json()
