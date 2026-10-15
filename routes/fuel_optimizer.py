import math

MAX_RANGE_MILES = 500.0
MPG = 10.0


def optimize_fuel_stops(
    route_distance_miles,
    stations,
    max_range=MAX_RANGE_MILES,
    mpg=MPG,
):
    """Choose reachable, cost-effective fuel stops along a route."""

    if route_distance_miles < 0 or max_range <= 0 or mpg <= 0:
        raise ValueError("Distance must be non-negative; range and MPG must be positive.")

    # Each station must have name, price, and route_distance_miles.
    stations = sorted(
        [
            dict(s)
            for s in stations
            if 0 < float(s["route_distance_miles"]) < route_distance_miles
            and float(s["price"]) > 0
        ],
        key=lambda s: float(s["route_distance_miles"]),
    )

    # Starting with a full tank, no stop is required for routes
    # within the vehicle's range.
    if route_distance_miles <= max_range:
        return {
            "stops": [],
            "gallons_required": round(route_distance_miles / mpg, 2),
            "total_fuel_cost_usd": 0.0,
            "cost_note": (
                "Cost excludes the starting full tank; its purchase "
                "price is unknown."
            ),
        }

    stops = []
    current_position = 0.0
    current_price = None
    total_cost = 0.0
    remaining = stations[:]

    while route_distance_miles - current_position > max_range:
        reachable = [
            s for s in remaining
            if current_position < float(s["route_distance_miles"])
            <= current_position + max_range
        ]

        if not reachable:
            raise ValueError(
                "No listed station is reachable within the 500-mile range."
            )

        # If we know the price at the current stop, prefer a cheaper
        # station ahead when it is reachable. Otherwise, choose the
        # cheapest reachable station.
        cheaper = (
            [
                s for s in reachable
                if current_price is not None
                and float(s["price"]) < current_price
            ]
        )

        if cheaper:
            chosen = min(
                cheaper,
                key=lambda s: float(s["route_distance_miles"]),
            )
        else:
            chosen = min(
                reachable,
                key=lambda s: (
                    float(s["price"]),
                    -float(s["route_distance_miles"]),
                ),
            )

        position = float(chosen["route_distance_miles"])
        price = float(chosen["price"])
        gallons = (position - current_position) / mpg

        # Estimate the fuel consumed between stops at the selected
        # station's price. This is a transparent approximation.
        total_cost += gallons * price

        stops.append({
            "name": chosen["name"],
            "route_distance_miles": round(position, 2),
            "price_per_gallon_usd": round(price, 3),
            "estimated_gallons": round(gallons, 2),
        })

        current_position = position
        current_price = price
        remaining = [
            s for s in remaining
            if float(s["route_distance_miles"]) > current_position
        ]

    final_leg = route_distance_miles - current_position
    if current_price is not None:
        total_cost += (final_leg / mpg) * current_price

    return {
        "stops": stops,
        "gallons_required": round(route_distance_miles / mpg, 2),
        "total_fuel_cost_usd": round(total_cost, 2),
        "cost_note": (
            "Approximate trip fuel cost; assumes fuel consumed on each "
            "leg is priced at the preceding selected stop. The starting "
            "tank cost is not included."
        ),
    }