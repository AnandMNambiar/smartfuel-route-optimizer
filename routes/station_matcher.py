from routes.fuel_data import load_fuel_prices
from routes.city_coordinates import get_city_coordinates
from routes.route_matching import nearest_route_position


# Small demo shortlist: do not geocode the entire CSV.
CANDIDATE_CITIES = [
    ("Dallas", "TX"),
    ("Hutchins", "TX"),
    ("Ennis", "TX"),
    ("Corsicana", "TX"),
    ("Madisonville", "TX"),
    ("Conroe", "TX"),
    ("Houston", "TX"),
]


def find_stations_near_route(route_geometry, max_distance_miles=10):
    coordinates = route_geometry.get("coordinates", [])

    if len(coordinates) < 2:
        raise ValueError("Invalid route geometry.")

    df = load_fuel_prices()
    stations = []

    df["city_clean"] = df["city"].astype(str).str.strip().str.lower()
    df["state_clean"] = df["state"].astype(str).str.strip().str.upper()

    for city, state in CANDIDATE_CITIES:
        matching_rows = df[
            (df["city_clean"] == city.lower())
            & (df["state_clean"] == state)
        ]

        if matching_rows.empty:
            continue

        try:
            city_coordinates = get_city_coordinates(city, state)
        except Exception:
            continue

        if city_coordinates is None:
            continue

        lat, lon = city_coordinates
        match = nearest_route_position(lat, lon, coordinates)

        if not match or match["distance_from_route_miles"] > max_distance_miles:
            continue

        cheapest = matching_rows.sort_values("retail_price").iloc[0]

        stations.append({
            "name": str(cheapest["truckstop_name"]),
            "city": city,
            "state": state,
            "price_per_gallon_usd": round(float(cheapest["retail_price"]), 3),
            "route_distance_miles": round(
                match["route_distance_miles"], 2
            ),
            "distance_from_route_miles": round(
                match["distance_from_route_miles"], 2
            ),
        })

    stations.sort(key=lambda station: station["route_distance_miles"])
    return stations