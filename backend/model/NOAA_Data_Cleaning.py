import pandas as pd

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

# Load the data, skipping the first two rows
df = pd.read_csv('us_states_avg_temp_1955_2025.csv', skiprows=2, names=['State', 'Date', 'Temp'])

# Drop any rows with 'Date' as a header or placeholder
df = df[df['Date'] != 'Date']

# Convert Temp to numeric, and drop invalid values
df['Temp'] = pd.to_numeric(df['Temp'], errors='coerce')
df = df.dropna(subset=['Temp'])

# Extract year from Date
df['Year'] = df['Date'].astype(str).str[:4].astype(int)

# Convert full state names to abbreviations
df['State'] = df['State'].map(state_abbrev)

# Drop rows where state name was unrecognized
df = df.dropna(subset=['State'])

# Group and calculate average temp
annual_avg = df.groupby(['State', 'Year'])['Temp'].mean().reset_index()

# Rename columns
annual_avg.columns = ['state_id', 'year', 'avg_temp']

# Save to CSV
annual_avg.to_csv('annual_state_avg_temp_1955_2025.csv', index=False)

print("✅ Saved annual averages with abbreviations and renamed columns to 'annual_state_avg_temp_1955_2024.csv'")
