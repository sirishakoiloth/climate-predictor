"""
from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)
model = joblib.load('model/climate_model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    year = data['year']
    state_id = data['state_id']

    # Prepare input
    input_df = pd.DataFrame({'year': [year], 'state_id': [state_id]})
    input_df = pd.get_dummies(input_df)

    # Ensure correct columns
    for col in model.feature_names_in_:
        if col not in input_df.columns:
            input_df[col] = 0
    input_df = input_df[model.feature_names_in_]

    prediction = model.predict(input_df)[0]
    return jsonify({'predicted_temp': round(prediction, 2)})

if __name__ == '__main__':
    app.run(debug=True)
"""

from flask import Flask, request, jsonify
import joblib
import numpy as np
from dotenv import load_dotenv
import os
import requests

# Load environment variables
load_dotenv()

# Load machine learning model
model = joblib.load("models/climate_model.pkl")

# Get API keys
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Set up Flask app
app = Flask(__name__)

# Route: Predict average temperature based on year and disaster count
@app.route('/predict', methods=['GET'])
def predict():
    year = request.args.get("year", type=int)
    disaster_count = request.args.get("disaster_count", type=int)

    if year is None or disaster_count is None:
        return jsonify({"error": "Missing year or disaster_count parameter"}), 400

    prediction = model.predict(np.array([[year, disaster_count]]))
    return jsonify({"predicted_temp": round(prediction[0], 2)})

# Route: Get current weather for a city using OpenWeatherMap API
@app.route('/weather', methods=['GET'])
def current_weather():
    city = request.args.get("city", default="Dallas")

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return jsonify({
            "city": city,
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"]
        })
    else:
        return jsonify({"error": "Failed to fetch weather data"}), response.status_code

# Run the server
if __name__ == '__main__':
    app.run(debug=True)
