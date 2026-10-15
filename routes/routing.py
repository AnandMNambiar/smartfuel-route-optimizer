from functools import lru_cache

import requests

OSRM_BASE_URL = "https://router.project-osrm.org"
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

HEADERS = {
    "User-Agent": "SmartFuelRouteOptimizer/1.0 (assessment project)"
}


@lru_cache(maxsize=256)
def geocode_location(location):
    """Convert a US place or address into longitude and latitude."""
    response = requests.get(
        NOMINATIM_URL,
        params={
            "q": f"{location}, USA",
            "format": "jsonv2",
            "limit": 1,
            "countrycodes": "us",
        },
        headers=HEADERS,
        timeout=15,
    )
    response.raise_for_status()
    results = response.json()

    if not results:
        raise ValueError(f"Could not locate US address: {location}")

    result = results[0]
    return float(result["lon"]), float(result["lat"])


def get_driving_route(start, finish):
    """Get a driving route and its geometry from OSRM."""
    start_lon, start_lat = geocode_location(start)
    finish_lon, finish_lat = geocode_location(finish)

    coordinates = (
        f"{start_lon},{start_lat};{finish_lon},{finish_lat}"
    )

    response = requests.get(
        f"{OSRM_BASE_URL}/route/v1/driving/{coordinates}",
        params={
            "overview": "full",
            "geometries": "geojson",
            "steps": "false",
        },
        timeout=25,
    )
    response.raise_for_status()
    data = response.json()

    if data.get("code") != "Ok" or not data.get("routes"):
        raise ValueError("No driving route was found.")

    route = data["routes"][0]

    return {
        "distance_miles": route["distance"] / 1609.344,
        "duration_hours": route["duration"] / 3600,
        "geometry": route["geometry"],
    }