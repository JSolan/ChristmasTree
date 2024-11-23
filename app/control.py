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
