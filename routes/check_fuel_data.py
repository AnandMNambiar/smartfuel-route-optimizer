from routes.fuel_data import load_fuel_prices

df = load_fuel_prices()

print("Rows loaded:", len(df))
print("Columns:", list(df.columns))
print("\nFirst 5 records:")
print(df.head().to_string(index=False))