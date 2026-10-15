from routes.routing import get_driving_route

route = get_driving_route("Dallas, Texas", "Houston, Texas")

print("Distance (miles):", round(route["distance_miles"], 2))
print("Duration (hours):", round(route["duration_hours"], 2))
print("Geometry type:", route["geometry"]["type"])
print(
    "Number of route coordinates:",
    len(route["geometry"]["coordinates"]),
)