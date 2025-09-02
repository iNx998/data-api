# pylint: disable=missing-module-docstring

import sys
import urllib.parse
import requests

BASE_URI = "https://weather.lewagon.com"


def search_city(query):
    """
    Search for a city using OpenWeatherMap's geocoding API.
    If multiple cities match, prompt the user to select one.
    Returns the selected city as a dictionary, or None if not found.
    """
    url = f"{BASE_URI}/geo/1.0/direct?q={urllib.parse.quote(query)}&limit=5"
    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        print("Failed to connect to the weather service.")
        return None

    cities = response.json()

    if not cities:
        print("City not found. Try again.")
        return None

    if len(cities) == 1:
        return cities[0]

    print("Multiple matches found, which city did you mean?")
    for i, city in enumerate(cities):
        name = city.get("name", "Unknown")
        country = city.get("country", "")
        print(f"{i + 1}. {name},{country}")

    while True:
        try:
            choice = int(input("> "))
            if 1 <= choice <= len(cities):
                return cities[choice - 1]
            print("Invalid choice. Try again.")
        except ValueError:
            print("Please enter a valid number.")
def weather_forecast(lat, lon):
    """
    Fetch 5-day weather forecast from the API for given lat/lon.
    Returns a list of daily forecasts (dicts with date, weather, and temp).
    """
    url = f"{BASE_URI}/data/2.5/forecast?lat={lat}&lon={lon}&units=metric"
    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        print("Failed to fetch weather data.")
        return []

    data = response.json()
    raw_forecasts = data.get("list", [])
    daily_forecast = {}

    for forecast in raw_forecasts:
        date = forecast['dt_txt'].split(" ")[0]
        temp = forecast['main']['temp_max']
        weather = forecast['weather'][0]['description']

        if date not in daily_forecast or daily_forecast[date]['temp'] < temp:
            daily_forecast[date] = {
                'date': date,
                'weather': weather.title(),
                'temp': round(temp, 1)
            }

    return list(daily_forecast.values())[:5]


def main():
    """
    Ask user for a city name, get forecast, and display it.
    Loops until user presses Ctrl-C.
    """
    query = input("City?\n> ")
    city = search_city(query)

    if not city:
        return

    print(f"Here's the weather in {city['name']}")
    forecast = weather_forecast(city['lat'], city['lon'])

    for day in forecast:
        print(f"{day['date']}: {day['weather']} {day['temp']}°C")


if __name__ == '__main__':
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print('\nGoodbye!')
        sys.exit(0)
