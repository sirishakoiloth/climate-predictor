import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

# Load data
df = pd.read_csv('../data/climate_data.csv')

# One-hot encode states
X = pd.get_dummies(df[['year', 'state_id']], columns=['state_id'])
y = df['avg_temp']

# Train model
model = LinearRegression()
model.fit(X, y)

# Save model
joblib.dump(model, 'model/climate_model.pkl')
print("✅ Model trained and saved.")
