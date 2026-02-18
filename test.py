import os
import requests
from dotenv import load_dotenv

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY").strip()

def get_weather(city: str) -> str:
    location_url = "http://dataservice.accuweather.com/locations/v1/cities/search"
    location_params = {"apikey": WEATHER_API_KEY, "q": city}

    response = requests.get(location_url, params=location_params)
    locations = response.json()

    if not locations:
        return "City not found."

    location_key = locations[0]["Key"]
    city_name = locations[0]["LocalizedName"]

    weather_url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}"
    weather_params = {"apikey": WEATHER_API_KEY, "details": True}

    weather_response = requests.get(weather_url, params=weather_params)
    data = weather_response.json()[0]

    temperature = data["Temperature"]["Metric"]["Value"]
    condition = data["WeatherText"]
    humidity = data["RelativeHumidity"]

    return (
        f"The current weather in {city_name} is {condition}. "
        f"The temperature is {temperature} degree Celsius "
        f"with humidity at {humidity} percent."
    )

print(get_weather("Regina"))