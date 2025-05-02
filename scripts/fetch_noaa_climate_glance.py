import pandas as pd
import requests
import io
import os

# NOAA state codes (not FIPS)
state_codes = {
    "AL": 1, "AZ": 2, "AR": 3, "CA": 4, "CO": 5, "CT": 6, "DE": 7,
    "FL": 8, "GA": 9, "ID": 10, "IL": 11, "IN": 12, "IA": 13,
    "KS": 14, "KY": 15, "LA": 16, "ME": 17, "MD": 18, "MA": 19,
    "MI": 20, "MN": 21, "MS": 22, "MO": 23, "MT": 24, "NE": 25,
    "NV": 26, "NH": 27, "NJ": 28, "NM": 29, "NY": 30, "NC": 31,
    "ND": 32, "OH": 33, "OK": 34, "OR": 35, "PA": 36, "RI": 37,
    "SC": 38, "SD": 39, "TN": 40, "TX": 41, "UT": 42, "VT": 43,
    "VA": 44, "WA": 45, "WV": 46, "WI": 47, "WY": 48
}

def fetch_state_temp(state_abbr, state_code):
    url = f"https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/statewide/time-series/{state_code}/tavg/ann/12/1895-2023.csv"
    print(f"Fetching data for {state_abbr}...")
    response = requests.get(url)
    if response.status_code == 200:
        df = pd.read_csv(io.StringIO(response.text), skiprows=4)
        df.columns = ["year", "avg_temp"]
        df["state"] = state_abbr
        return df
    else:
        print(f"Failed to fetch {state_abbr}")
        return pd.DataFrame()

def compile_all_states():
    all_data = []
    for abbr, code in state_codes.items():
        df = fetch_state_temp(abbr, code)
        if not df.empty:
            all_data.append(df)
    combined = pd.concat(all_data, ignore_index=True)
    os.makedirs("data/processed/", exist_ok=True)
    combined.to_csv("data/processed/noaa_all_states_temp.csv", index=False)
    print("Saved: data/processed/noaa_all_states_temp.csv")

if __name__ == "__main__":
    compile_all_states()
