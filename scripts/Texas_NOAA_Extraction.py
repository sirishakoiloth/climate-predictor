import pandas as pd
import os

# Step 1: Load raw NOAA data
input_path = "data/raw/Texas_NOAA.csv"
df = pd.read_csv(input_path, comment="#")

# Step 2: Clean data
df["Value"] = df["Value"].replace(-99, pd.NA)
df = df.dropna(subset=["Value"])
df["Date"] = df["Date"].astype(str)
df["Year"] = df["Date"].str[:4].astype(int)

# Step 3: Compute annual average temperature in Fahrenheit
annual_avg = df.groupby("Year")["Value"].mean().reset_index()
annual_avg.rename(columns={"Value": "avg_temp"}, inplace=True)

# Step 4: Add state abbreviation ("TX")
annual_avg["state_id"] = "TX"

# Step 5: Reorder columns
final_df = annual_avg[["state_id", "Year", "avg_temp"]]
final_df.rename(columns={"Year": "year"}, inplace=True)

# Step 6: Save to CSV
output_path = "data/processed/Texas_NOAA_processed.csv"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
final_df.to_csv(output_path, index=False)

print(f"✅ Saved processed file: {output_path}")
