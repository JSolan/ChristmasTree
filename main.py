import os
from dotenv import load_dotenv
from flask import Flask, render_template, request
from app.api import WLEDAPI
from app.control import reset_segment_and_apply_effect
from app.WLED_data import get_effects_and_palettes

# Load environment variables from .env
load_dotenv()
WLED_IP = os.getenv("WLED_IP")

if not WLED_IP:
    raise ValueError("WLED_IP is not set in the .env file")

# Initialize Flask app and WLED API
app = Flask(__name__)
api = WLEDAPI(WLED_IP)

@app.route("/", methods=["GET", "POST"])
def index():
    # Fetch dynamic data
    effects, palettes = get_effects_and_palettes(api)

    if request.method == "POST":
        effect_id = int(request.form.get("effect_id"))
        palette_id = int(request.form.get("palette_id"))
        brightness = int(request.form.get("brightness"))
        led_count = int(request.form.get("led_count"))
        
        # Apply effect with the selected parameters
        payload = {
            "on": True,
            "bri": brightness,
            "seg": [
                {
                    "id": 0,
                    "start": 0,
                    "stop": led_count,
                    "fx": effect_id,
                    "pal": palette_id,
                    "frz": False
                }
            ]
        }
        api.set_state(payload)

    return render_template("index.html", effects=effects, palettes=palettes)

if __name__ == "__main__":
    app.run(debug=True)
