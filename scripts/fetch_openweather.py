import requests
import os
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime

load_dotenv()
api_key = os.getenv("OPENWEATHER_API_KEY")

def get_current_weather(city="Dallas"):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "city": city,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "weather": data["weather"][0]["description"]
        }
    else:
        print(f"Failed to fetch weather for {city}: {response.status_code}")
        return None

def save_weather_to_csv(city="Dallas"):
    data = get_current_weather(city)
    if data:
        df = pd.DataFrame([data])
        output_path = "data/raw/openweather_now.csv"

        # Create header if file doesn't exist
        write_header = not os.path.exists(output_path)

        df.to_csv(output_path, mode='a', index=False, header=write_header)
        print(f"Saved weather data for {city} at {data['timestamp']}")

if __name__ == "__main__":
    save_weather_to_csv("Dallas")
