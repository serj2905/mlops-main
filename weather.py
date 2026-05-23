import csv
import os
from datetime import datetime

import requests
from dotenv import load_dotenv


CSV_PATH = "weather.csv"
CITY = "Moscow"


def fetch_weather(city: str = CITY) -> dict:
    """Получает текущую погоду по городу через OpenWeatherMap."""
    load_dotenv()

    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise ValueError("Не найден OPENWEATHER_API_KEY. Добавьте ключ в .env")

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
        "lang": "ru",
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    return response.json()


def save_weather() -> str:
    """Записывает новую строку с погодой в weather.csv."""
    data = fetch_weather()

    row = {
        "datetime": datetime.fromtimestamp(data["dt"]).strftime("%Y-%m-%d %H:%M:%S"),
        "city": data["name"],
        "weather_main": data["weather"][0]["main"],
        "weather_description": data["weather"][0]["description"],
        "temp": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "pressure": data["main"]["pressure"],
        "wind_speed": data["wind"]["speed"],
    }

    file_exists = os.path.exists(CSV_PATH)

    with open(CSV_PATH, "a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())

        if not file_exists or os.path.getsize(CSV_PATH) == 0:
            writer.writeheader()

        writer.writerow(row)

    return CSV_PATH
