"""
jarvis/weather.py — Weather Service
Fetches real-time weather data from AccuWeather API.
"""

import requests
from config import WEATHER_API_KEY

BASE_URL = "http://dataservice.accuweather.com"


def get_weather(city: str) -> dict:
    """
    Fetch current weather for a city.

    Args:
        city: City name to search for.

    Returns:
        Dict with keys: city, condition, temperature, humidity
        Or dict with key: error (on failure)
    """
    if not WEATHER_API_KEY:
        return {"error": "Weather API key not configured."}

    try:
        # Step 1: Get location key
        loc_resp = requests.get(
            f"{BASE_URL}/locations/v1/cities/search",
            params={"apikey": WEATHER_API_KEY, "q": city},
            timeout=8,
        )
        locations = loc_resp.json()

        if not locations:
            return {"error": f"City '{city}' not found."}

        location_key = locations[0]["Key"]
        city_name    = locations[0]["LocalizedName"]

        # Step 2: Get current conditions
        wx_resp = requests.get(
            f"{BASE_URL}/currentconditions/v1/{location_key}",
            params={"apikey": WEATHER_API_KEY, "details": True},
            timeout=8,
        )
        data = wx_resp.json()[0]

        return {
            "city":        city_name,
            "condition":   data["WeatherText"],
            "temperature": data["Temperature"]["Metric"]["Value"],
            "humidity":    data["RelativeHumidity"],
        }

    except Exception as e:
        print(f"[Weather Error]: {e}")
        return {"error": "Could not fetch weather right now."}


def format_weather(data: dict) -> str:
    """
    Convert weather dict to a speakable string.

    Args:
        data: Dict returned by get_weather()

    Returns:
        Human-readable weather string.
    """
    if "error" in data:
        return data["error"]

    return (
        f"The current weather in {data['city']} is {data['condition']}. "
        f"Temperature is {data['temperature']}°C "
        f"with humidity at {data['humidity']}%."
    )