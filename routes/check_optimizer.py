from routes.fuel_optimizer import optimize_fuel_stops

stations = [
    {
        "name": "Station A",
        "price": 3.50,
        "route_distance_miles": 300,
    },
    {
        "name": "Station B",
        "price": 3.10,
        "route_distance_miles": 450,
    },
    {
        "name": "Station C",
        "price": 3.80,
        "route_distance_miles": 700,
    },
    {
        "name": "Station D",
        "price": 3.20,
        "route_distance_miles": 900,
    },
]

result = optimize_fuel_stops(
    route_distance_miles=1200,
    stations=stations,
)

print(result)