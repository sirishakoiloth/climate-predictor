import pandas as pd
import os

def process_state_temperature():
    os.makedirs("data/processed/", exist_ok=True)
    df = pd.read_csv("data/raw/climdiv_state_year.csv")
    df = df.rename(columns={"temperature": "avg_temp"})
    df = df[["state", "year", "avg_temp"]]
    df.to_csv("data/processed/temp_by_state_year.csv", index=False)
    print("✅ Processed state-level annual temperature data")

if __name__ == "__main__":
    process_state_temperature()
