import pandas as pd
import os

# Map FIPS to 2-letter state codes
fips_to_state = {
    1: "AL", 2: "AZ", 3: "AR", 4: "CA", 5: "CO", 6: "CT", 7: "DE",
    8: "FL", 9: "GA", 10: "ID", 11: "IL", 12: "IN", 13: "IA",
    14: "KS", 15: "KY", 16: "LA", 17: "ME", 18: "MD", 19: "MA",
    20: "MI", 21: "MN", 22: "MS", 23: "MO", 24: "MT", 25: "NE",
    26: "NV", 27: "NH", 28: "NJ", 29: "NM", 30: "NY", 31: "NC",
    32: "ND", 33: "OH", 34: "OK", 35: "OR", 36: "PA", 37: "RI",
    38: "SC", 39: "SD", 40: "TN", 41: "TX", 42: "UT", 43: "VT",
    44: "VA", 45: "WA", 46: "WV", 47: "WI", 48: "WY"
}

def process_state_temperature():
    os.makedirs("data/processed/", exist_ok=True)
    df = pd.read_csv("data/raw/climdiv_state_year.csv")
    
    df = df.rename(columns={"fips": "fips", "year": "year", "tempc": "avg_temp"})
    df["state"] = df["fips"].map(fips_to_state)

    df = df[["state", "year", "avg_temp"]].dropna()
    df.to_csv("data/processed/temp_by_state_year.csv", index=False)
    print("Processed state-level annual temperature data")

if __name__ == "__main__":
    process_state_temperature()

