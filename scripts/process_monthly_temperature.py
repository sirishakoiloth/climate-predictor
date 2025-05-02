import pandas as pd
import os

def process_monthly_temperature():
    os.makedirs("data/processed/", exist_ok=True)
    df = pd.read_csv("data/raw/Average_temperature_by_state_2000_2021.csv")
    df = df.rename(columns={"Year": "year"})
    monthly_avg = df.groupby(["State", "year"]).mean(numeric_only=True).reset_index()
    monthly_avg.columns = [col.lower().strip().replace(" ", "_") for col in monthly_avg.columns]
    monthly_avg = monthly_avg.rename(columns={"state": "state"})
    monthly_avg.to_csv("data/processed/monthly_temp_by_state.csv", index=False)
    print("Processed monthly average temperature by state")

if __name__ == "__main__":
    process_monthly_temperature()
