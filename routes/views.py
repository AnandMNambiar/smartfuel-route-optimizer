from rest_framework.decorators import api_view
from rest_framework.response import Response

from routes.routing import get_driving_route
from routes.fuel_data import load_fuel_prices
from routes.station_matcher import find_stations_near_route


@api_view(["POST"])
def optimize_route(request):
    start = request.data.get("start")
    finish = request.data.get("finish")

    if not isinstance(start, str) or not start.strip():
        return Response(
            {"error": "Enter a valid start location."},
            status=400,
        )

    if not isinstance(finish, str) or not finish.strip():
        return Response(
            {"error": "Enter a valid finish location."},
            status=400,
        )

    try:
        start = start.strip()
        finish = finish.strip()

        route = get_driving_route(start, finish)
        fuel_data = load_fuel_prices()
        stations = find_stations_near_route(route["geometry"])

        distance = route["distance_miles"]
        gallons_required = distance / 10

        if stations:
            average_price = sum(
                station["price_per_gallon_usd"]
                for station in stations
            ) / len(stations)

            fuel_cost = round(gallons_required * average_price, 2)
        else:
            average_price = None
            fuel_cost = None

        return Response({
            "start": start,
            "finish": finish,
            "distance_miles": round(distance, 2),
            "duration_hours": round(route["duration_hours"], 2),
            "fuel_efficiency_mpg": 10,
            "maximum_range_miles": 500,
            "gallons_required": round(gallons_required, 2),
            "fuel_stops": stations,
            "fuel_price_records_loaded": len(fuel_data),
            "average_fuel_price_usd": (
                round(average_price, 3)
                if average_price is not None
                else None
            ),
            "fuel_cost_usd": fuel_cost,
            "cost_note": (
                "Estimated trip fuel cost using the average price of "
                "the matched station candidates. This is an estimate, "
                "not a verified minimum-cost refuelling plan. "
                "Station locations use approximate city-center coordinates."
            ),
            "route_geometry": route["geometry"],
        })

    except ValueError as exc:
        return Response({"error": str(exc)}, status=400)

    except Exception:
        return Response(
            {"error": "Route calculation or fuel-station matching failed."},
            status=502,
        )
