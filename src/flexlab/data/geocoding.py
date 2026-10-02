"""Geocoding: place name -> coordinates (OpenStreetMap Nominatim)."""

import requests

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
# Nominatim requires an identifying User-Agent. Replace DEIN-NAME with your GitHub name.
USER_AGENT = "flexlab/0.1 (github.com/DEIN-NAME/flexlab)"


def geocode(place: str, country_code: str | None = None) -> dict:
    """Return latitude, longitude and display name for a place name.

    Raises ValueError if the place is not found.
    """
    params = {"q": place, "format": "json", "limit": 1}
    if country_code:
        params["countrycodes"] = country_code
    response = requests.get(
        NOMINATIM_URL,
        params=params,
        headers={"User-Agent": USER_AGENT},
        timeout=10,
    )
    response.raise_for_status()
    results = response.json()
    if not results:
        raise ValueError(f"Place not found: {place}")
    hit = results[0]
    return {
        "latitude": float(hit["lat"]),
        "longitude": float(hit["lon"]),
        "name": hit["display_name"],
    }