from app.api import WLEDAPI

def get_effects_and_palettes(api):
    """
    Fetch effects and palettes from the WLED device.
    :param api: Instance of WLEDAPI.
    :return: Tuple of (effects, palettes).
    """
    effects = {}
    palettes = {}

    try:
        response = api.get_state()
        # Effects are returned as a list; map them to indices
        effects = {idx: effect for idx, effect in enumerate(response.get("effects", []))}
        # Palettes are returned as a list; map them to indices
        palettes = {idx: palette for idx, palette in enumerate(response.get("palettes", []))}
    except Exception as e:
        print(f"Error fetching effects and palettes: {e}")

    return effects, palettes
