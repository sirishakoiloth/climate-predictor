import requests
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
NOAA_TOKEN = os.getenv("NOAA_TOKEN")

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
        if response.status_code == 200 and "results" in response.json():
            df = pd.DataFrame(response.json()["results"])
            df["year"] = year
            results.append(df)

    final_df = pd.concat(results, ignore_index=True)
    final_df.to_csv("data/raw/noaa_temp_texas.csv", index=False)

def fetch_fema_disasters():
    fema_url = "https://www.fema.gov/api/open/v2/DisasterDeclarationsSummaries?$format=csv"
    fema_df = pd.read_csv(fema_url)
    fema_df.to_csv("data/raw/fema_disasters.csv", index=False)

if __name__ == "__main__":
    fetch_noaa_temperature("48")  # FIPS code for Texas
    fetch_fema_disasters()
