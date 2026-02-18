import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = "WEATHER_API_KEY"   # replace with your real key

def get_weather(city: str) -> str:
    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(url, params=params)
        print(response.status_code)

        if response.status_code != 200:
            return "Sorry, I couldn't fetch the weather right now."

        data = response.json()

        city_name = data["name"]
        temperature = data["main"]["temp"]
        condition = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]

        return (
            f"The current weather in {city_name} is {condition}. "
            f"The temperature is {temperature} degree Celsius "
            f"with humidity at {humidity} percent."
        )

    except:
        return "Sorry, there was an error getting the weather."


print(get_weather("New York"))