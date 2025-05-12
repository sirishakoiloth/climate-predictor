import pandas as pd
import os

# Create the processed directory if it doesn't exist
os.makedirs("data/processed", exist_ok=True)

# Mapping from full state names to abbreviations
state_abbrev = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
    'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE',
    'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID',
    'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS',
    'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
    'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
    'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV',
    'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY',
    'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK',
    'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
    'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT',
    'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV',
    'Wisconsin': 'WI', 'Wyoming': 'WY'
}

# Load the raw CSV file
df = pd.read_csv('data/raw/us_states_avg_temp_1955_2025.csv', skiprows=2, names=['State', 'Date', 'Temp'])

# Drop any rows with 'Date' as a placeholder
df = df[df['Date'] != 'Date']

# Convert Temp to numeric and drop invalid
df['Temp'] = pd.to_numeric(df['Temp'], errors='coerce')
df = df.dropna(subset=['Temp'])

# Extract year from Date
df['Year'] = df['Date'].astype(str).str[:4].astype(int)

# Convert state names to abbreviations
df['State'] = df['State'].map(state_abbrev)
df = df.dropna(subset=['State'])

# Group by state and year
annual_avg = df.groupby(['State', 'Year'])['Temp'].mean().reset_index()
annual_avg.columns = ['state_id', 'year', 'avg_temp']

# Save processed CSV
processed_path = 'data/processed/annual_state_avg_temp_1955_2025.csv'
annual_avg.to_csv(processed_path, index=False)

print(f"✅ Saved processed CSV to {processed_path}")
