import math


EARTH_RADIUS_MILES = 3958.8


def haversine_miles(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(
        math.radians, [lat1, lon1, lat2, lon2]
    )

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(dlon / 2) ** 2
    )

    return 2 * EARTH_RADIUS_MILES * math.asin(
        math.sqrt(min(1.0, a))
    )


def nearest_route_position(station_lat, station_lon, route_coordinates):
    if len(route_coordinates) < 2:
        return None

    cumulative_miles = 0.0
    best_match = None

    for index in range(len(route_coordinates) - 1):
        lon1, lat1 = route_coordinates[index]
        lon2, lat2 = route_coordinates[index + 1]

        segment_length = haversine_miles(lat1, lon1, lat2, lon2)

        # Approximate the segment in local miles-based coordinates.
        mean_lat = math.radians((lat1 + lat2) / 2)
        x_scale = 69.172 * math.cos(mean_lat)
        y_scale = 69.0

        ax, ay = lon1 * x_scale, lat1 * y_scale
        bx, by = lon2 * x_scale, lat2 * y_scale
        px, py = station_lon * x_scale, station_lat * y_scale

        dx, dy = bx - ax, by - ay
        length_squared = dx * dx + dy * dy

        if length_squared == 0:
            fraction = 0.0
        else:
            fraction = (
                (px - ax) * dx + (py - ay) * dy
            ) / length_squared
            fraction = max(0.0, min(1.0, fraction))

        nearest_lat = lat1 + fraction * (lat2 - lat1)
        nearest_lon = lon1 + fraction * (lon2 - lon1)

        distance_from_route = haversine_miles(
            station_lat, station_lon, nearest_lat, nearest_lon
        )

        if (
            best_match is None
            or distance_from_route < best_match["distance_from_route_miles"]
        ):
            best_match = {
                "route_distance_miles": cumulative_miles
                + fraction * segment_length,
                "distance_from_route_miles": distance_from_route,
            }

        cumulative_miles += segment_length

    return best_match