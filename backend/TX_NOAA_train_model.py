import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
import os

# Load the processed NOAA dataset for Texas
df = pd.read_csv('../data/Texas_NOAA_processed.csv')  # Adjust path as needed

# One-hot encode the 'state_id' column (in this case, it's always "TX")
X = pd.get_dummies(df[['year', 'state_id']], columns=['state_id'])

# Target variable: average temperature
y = df['avg_temp']

# Train the linear regression model
model = LinearRegression()
model.fit(X, y)

# Ensure output directory exists
os.makedirs('model', exist_ok=True)

# Save the trained model
joblib.dump(model, 'model/TX_NOAA_climate_model.pkl')

print("Model trained and saved at model/TX_NOAA_climate_model.pkl")
