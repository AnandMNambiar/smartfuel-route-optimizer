# SmartFuel Route Optimizer

A Django REST API that calculates driving routes and estimates fuel costs using OpenStreetMap routing and a fuel-price dataset.

## Features

- Calculates driving distance and estimated duration.
- Uses OSRM for driving-route information.
- Geocodes start and finish locations using OpenStreetMap Nominatim.
- Loads fuel-price data from a CSV file.
- Identifies candidate fuel stations near the route.
- Estimates fuel consumption using 10 MPG.
- Includes route geometry in the API response.

## Tech Stack

- Python 3.11
- Django
- Django REST Framework
- Pandas
- Requests
- Geopy
- OSRM and OpenStreetMap

## Setup

Clone the repository:

```bash
git clone https://github.com/AnandMNambiar/smartfuel-route-optimizer.git
cd smartfuel-route-optimizer
```

Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install django djangorestframework requests pandas geopy
```

Run the Django development server:

```bash
python manage.py runserver
```

## API Usage

**Endpoint:** `POST /api/optimize/`

Example JSON request:

```json
{
  "start": "Dallas, Texas",
  "finish": "Houston, Texas"
}
```

The response includes route distance, duration, estimated gallons required, candidate fuel stations, estimated fuel cost, and route geometry.

## Assumptions and Limitations

- Fuel efficiency is assumed to be 10 miles per gallon.
- Maximum vehicle range is 500 miles.
- Fuel costs are estimates based on candidate station prices, not a guaranteed minimum-cost refuelling plan.
- Station matching uses approximate city-center coordinates.
- The current candidate-city shortlist is limited to selected cities in Texas.
- Routing and geocoding depend on external services.

## Data

Fuel-price records are loaded from `data/fuel_prices.csv`.

## Disclaimer

Fuel prices, station matches, travel distances, and cost estimates may vary. This project is a prototype for route and fuel-cost estimation.
