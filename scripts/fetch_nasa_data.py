import pandas as pd
import os

def process_nasa_temperature():
    file_path = "data/raw/nasa_global_temp.csv"
    df = pd.read_csv(file_path, skiprows=1)  
    df.columns = ["Year", "Annual Anomaly (°C)"]
    df = df.dropna()
    df["Year"] = df["Year"].astype(int)
    df.rename(columns={"Annual Anomaly (°C)": "temp_anomaly"}, inplace=True)
    df.to_csv("data/processed/nasa_temp_processed.csv", index=False)
    print("NASA global temperature anomalies processed.")

def process_mauna_loa_co2():
    file_path = "data/raw/mauna_loa_co2_monthly.csv"
    df = pd.read_csv(file_path, comment="#", header=None, delim_whitespace=True)
    df.columns = ["year", "month", "decimal_date", "average", "interpolated", "trend", "days"]
    co2_yearly = df.groupby("year")["interpolated"].mean().reset_index()
    co2_yearly.rename(columns={"interpolated": "co2_ppm"}, inplace=True)
    co2_yearly.to_csv("data/processed/co2_yearly_avg.csv", index=False)
    print("Mauna Loa CO₂ data processed.")

if __name__ == "__main__":
    os.makedirs("data/processed/", exist_ok=True)
    process_nasa_temperature()
    process_mauna_loa_co2()
