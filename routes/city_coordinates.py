from functools import lru_cache

from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

geolocator = Nominatim(
    user_agent="smartfuel_route_optimizer_assessment"
)

geocode = RateLimiter(
    geolocator.geocode,
    min_delay_seconds=1.1,
    swallow_exceptions=False,
)


@lru_cache(maxsize=512)
def get_city_coordinates(city, state):
    query = f"{city}, {state}, USA"

    location = geocode(
        query,
        country_codes="us",
        exactly_one=True,
        timeout=10,
    )

    if location is None:
        return None

    return (location.latitude, location.longitude)