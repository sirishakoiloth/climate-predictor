import os
import subprocess
import sys

# Ensure python-dotenv is installed
try:
    from dotenv import load_dotenv
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-dotenv"])
    from dotenv import load_dotenv

import requests
import pandas as pd

load_dotenv()
NOAA_TOKEN = os.getenv("NOAA_TOKEN")

# Ensure the output directory exists
os.makedirs("data/raw", exist_ok=True)

def fetch_noaa_temperature(state_fips, start_year=2010, end_year=2020):
    headers = {"token": NOAA_TOKEN}
    base_url = "https://www.ncei.noaa.gov/cdo-web/api/v2/data"
    results = []

    for year in range(start_year, end_year + 1):
        params = {
            "datasetid": "GHCND",
            "locationid": f"FIPS:{state_fips}",
            "datatypeid": "TAVG",
            "startdate": f"{year}-01-01",
            "enddate": f"{year}-12-31",
            "limit": 1000
        }
        response = requests.get(base_url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            if "results" in data:
                df = pd.DataFrame(data["results"])
                df["year"] = year
                results.append(df)
            else:
                print(f"No results found for year {year}.")
        else:
            print(f"Failed to fetch data for year {year}. Status code: {response.status_code}")

    if results:
        final_df = pd.concat(results, ignore_index=True)
        final_df.to_csv("data/raw/noaa_temp_texas.csv", index=False)
        print("Data successfully saved to data/raw/noaa_temp_texas.csv")
    else:
        print("No data fetched. The results list is empty.")

def fetch_fema_disasters():
    fema_url = "https://www.fema.gov/api/open/v2/DisasterDeclarationsSummaries?$format=csv"
    fema_df = pd.read_csv(fema_url)
    fema_df.to_csv("data/raw/fema_disasters.csv", index=False)

if __name__ == "__main__":
    fetch_noaa_temperature("48")  # FIPS code for Texas
    fetch_fema_disasters()
