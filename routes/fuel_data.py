from pathlib import Path

import pandas as pd
from django.conf import settings

FUEL_CSV_PATH = (
    Path(settings.BASE_DIR) / "data" / "fuel_prices.csv"
)


def load_fuel_prices():
    """Load and validate the supplied fuel-price dataset."""
    if not FUEL_CSV_PATH.exists():
        raise FileNotFoundError(
            f"Fuel-price CSV not found: {FUEL_CSV_PATH}"
        )

    df = pd.read_csv(FUEL_CSV_PATH)
    df.columns = [
        column.strip().lower().replace(" ", "_")
        for column in df.columns
    ]

    required_columns = {"retail_price"}
    missing = required_columns - set(df.columns)

    if missing:
        raise ValueError(
            f"Missing required CSV columns: {sorted(missing)}. "
            f"Available columns: {list(df.columns)}"
        )

    df["retail_price"] = pd.to_numeric(
        df["retail_price"], errors="coerce"
    )
    df = df.dropna(subset=["retail_price"])
    df = df[df["retail_price"] > 0].copy()

    return df
