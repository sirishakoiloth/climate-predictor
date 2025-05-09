import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

# Load data
df = pd.read_csv('../data/annual_state_avg_temp_1955_2025.csv')

# One-hot encode states
X = pd.get_dummies(df[['year', 'state_id']], columns=['state_id'])
y = df['avg_temp']

# Train model
model = LinearRegression()
model.fit(X, y)

# Save model
joblib.dump(model, 'model/NOAA_climate_model.pkl')
print("✅ Model trained and saved.")