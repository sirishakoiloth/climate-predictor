import pandas as pd
import os

def process_monthly_temperature():
    os.makedirs("data/processed/", exist_ok=True)

    df = pd.read_csv("data/raw/average_monthly_temperature_by_state_1950-2022.csv")

    # Normalize column names
    df.columns = [col.lower().strip() for col in df.columns]

    # Clean state name to consistent format (e.g., uppercase abbreviation)
    state_abbr = {
        'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
        'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
        'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
        'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
        'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
        'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH',
        'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC',
        'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA',
        'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN',
        'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA',
        'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
    }

    df["state"] = df["state"].map(state_abbr)

    # Group by state and year to get annual average of monthly temperatures
    result = df.groupby(["state", "year"])["average_temp"].mean().reset_index()
    result = result.rename(columns={"average_temp": "annual_avg_temp"})

    result.to_csv("data/processed/monthly_temp_by_state.csv", index=False)
    print("Processed monthly average temperature by state")

if __name__ == "__main__":
    process_monthly_temperature()

