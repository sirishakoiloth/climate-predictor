import requests
import csv
import time
import os

# Ensure the directory exists
os.makedirs('data/raw', exist_ok=True)

# List of (state_id, state_name) from NOAA's state codes (1–48 for contiguous U.S.)
states = [
    (1, 'Alabama'), (2, 'Arizona'), (3, 'Arkansas'), (4, 'California'), (5, 'Colorado'),
    (6, 'Connecticut'), (7, 'Delaware'), (8, 'Florida'), (9, 'Georgia'), (10, 'Idaho'),
    (11, 'Illinois'), (12, 'Indiana'), (13, 'Iowa'), (14, 'Kansas'), (15, 'Kentucky'),
    (16, 'Louisiana'), (17, 'Maine'), (18, 'Maryland'), (19, 'Massachusetts'), (20, 'Michigan'),
    (21, 'Minnesota'), (22, 'Mississippi'), (23, 'Missouri'), (24, 'Montana'), (25, 'Nebraska'),
    (26, 'Nevada'), (27, 'New Hampshire'), (28, 'New Jersey'), (29, 'New Mexico'), (30, 'New York'),
    (31, 'North Carolina'), (32, 'North Dakota'), (33, 'Ohio'), (34, 'Oklahoma'), (35, 'Oregon'),
    (36, 'Pennsylvania'), (37, 'Rhode Island'), (38, 'South Carolina'), (39, 'South Dakota'),
    (40, 'Tennessee'), (41, 'Texas'), (42, 'Utah'), (43, 'Vermont'), (44, 'Virginia'),
    (45, 'Washington'), (46, 'West Virginia'), (47, 'Wisconsin'), (48, 'Wyoming')
]

base_url = "https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/statewide/time-series"
start_year = 1955
end_year = 2025

output_file = 'data/raw/us_states_avg_temp_1955_2025.csv'

with open(output_file, mode='w', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['State', 'Year', 'Average Temperature (F)'])

    for state_id, state_name in states:
        url = f"{base_url}/{state_id}/tavg/1/0/{start_year}-{end_year}.csv"
        print(f"Fetching: {state_name} ...")

        try:
            response = requests.get(url)
            response.raise_for_status()
            lines = response.text.splitlines()

            for line in lines:
                if line.startswith("#") or not line.strip():
                    continue
                parts = line.split(",")
                if len(parts) >= 2:
                    year = parts[0]
                    temp = parts[1]
                    if temp != "-99":
                        writer.writerow([state_name, year, temp])
        except Exception as e:
            print(f"Error fetching data for {state_name}: {e}")

        time.sleep(1)  # Be nice to the server

print(f"\n✅ CSV saved as: {output_file}")
