def set_led_colors(api, colors):
    """
    Sets specific colors on the WLED device.
    :param api: Instance of WLEDAPI.
    :param colors: List of [index, r, g, b] for LEDs.
    """
    payload = {"seg": [{"i": colors}]}
    return api.set_state(payload)

def apply_effect(api, effect_id):
    """
    Apply a built-in WLED effect.
    :param api: Instance of WLEDAPI.
    :param effect_id: Integer ID of the effect.
    """
    payload = {"seg": [{"fx": effect_id}]}
    return api.set_state(payload)

def reset_segment_and_apply_effect(api, effect_id, palette_id=0, led_count=50):
    """
    Reset WLED segment configuration and apply an effect.
    :param api: Instance of WLEDAPI.
    :param effect_id: WLED effect ID to apply.
    :param palette_id: WLED palette ID to apply.
    :param led_count: Total number of LEDs in the strip.
    """
    payload = {
        "on": True,  # Ensure LEDs are powered on
        "bri": 255,  # Set maximum brightness
        "seg": [
            {
                "id": 0,         # Segment ID
                "start": 0,      # Start of segment
                "stop": led_count,  # End of segment
                "fx": effect_id,  # Effect ID
                "pal": palette_id,  # Palette ID
                "frz": False    # Unfreeze the segment
            }
        ]
    }
    api.set_state(payload)