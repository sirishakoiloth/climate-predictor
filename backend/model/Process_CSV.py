import pandas as pd
import requests
import os

# Step 1: Download the raw Texas_NOAA.csv file from GitHub
url = "https://raw.githubusercontent.com/your-username/your-repo-name/main/data/Texas_NOAA.csv"
response = requests.get(url)

# Save the raw file locally in the data folder
raw_file_path = "../data/Texas_NOAA.csv"
with open(raw_file_path, "wb") as f:
    f.write(response.content)

print(f"Downloaded raw file: {raw_file_path}")

# Step 2: Load and clean the raw data
df = pd.read_csv(raw_file_path, comment="#")
df["Value"] = df["Value"].replace(-99, pd.NA)  # Replace -99 with NaN
df = df.dropna(subset=["Value"])  # Drop rows with NaN values
df["Date"] = df["Date"].astype(str)  # Ensure Date is a string
df["Year"] = df["Date"].str[:4].astype(int)  # Extract Year from Date

# Step 3: Compute annual average temperature
annual_avg = df.groupby("Year")["Value"].mean().reset_index()
annual_avg.rename(columns={"Value": "avg_temp"}, inplace=True)

# Add state abbreviation ("TX")
annual_avg["state_id"] = "TX"

# Reorder columns
final_df = annual_avg[["state_id", "Year", "avg_temp"]]
final_df.rename(columns={"Year": "year"}, inplace=True)

# Step 4: Save the processed data to the data folder
processed_file_path = "../data/Texas_NOAA_processed.csv"
final_df.to_csv(processed_file_path, index=False)

print(f"✅ Saved processed file: {processed_file_path}")

# Step 5: (Optional) Commit and push the processed file to GitHub using Git
# You can automate this step using Git commands:
# git add ../data/Texas_NOAA_processed.csv
# git commit -m "Add processed NOAA data file"
# git push origin main
