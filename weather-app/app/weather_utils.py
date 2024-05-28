from countries import COUNTRIES, CAPITALS
from dotenv import load_dotenv
import os  # environ
import requests  # get()
import exceptions

# Constants
DAY = 24
MORNING = 12
NIGHT = 23
DATE_LEN = 10
WEEK = 7


def get_geo(location: str) -> dict:
    # Importing the api key from the .env file
    load_dotenv()
    api_key = os.environ['API_KEY']
    if location.lower() in COUNTRIES:
        geo_url = (f"http://api.openweathermap.org/geo/1.0/direct?q={CAPITALS[location.lower()]},"
                   f"{COUNTRIES[location.lower()]}&appid={api_key}")
    else:
        # Getting the geo info (country, city, lat and lon)
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={location}&appid={api_key}"
    geo_resp = requests.get(geo_url)
    # Checking for errors
    if geo_resp.status_code not in range(200, 300):
        raise exceptions.DataError
    # Parsing the geo data
    geo_data = geo_resp.json()
    if not geo_data:
        raise exceptions.LocationError
    lon, lat = geo_data[0]['lon'], geo_data[0]['lat']
    location = f"{geo_data[0]['country']}, {geo_data[0]['name']}"
    return {'location': location,
            'lon': lon,
            'lat': lat
            }


def get_weather_data(location: str) -> dict:
    geo_data = get_geo(location)
    # Getting the weather data
    url = (f"https://api.open-meteo.com/v1/forecast?latitude={geo_data['lat']}&longitude={geo_data['lon']}"
           f"&hourly=temperature_2m,relative_humidity_2m&timezone=auto")
    resp = requests.get(url)
    # Checking for errors
    if resp.status_code not in range(200, 300):
        raise exceptions.DataError
    # Parsing the weather data
    data = resp.json()
    if not data:
        raise exceptions.LocationError
    i = 0
    # Calculating average humidity per day
    avg_humidity = []
    while i + DAY <= len(data['hourly']['relative_humidity_2m']):
        avg_humidity.append(sum(data['hourly']['relative_humidity_2m'][i:i + DAY]) / DAY)
        i += DAY

    # Organizing the dates, day and night temperatures in lists
    dates = []
    day_temp = []
    night_temp = []
    for i in range(WEEK):
        curr_time = data['hourly']['time'][i * DAY][:DATE_LEN]
        dates.append(curr_time[8:] + curr_time[4:8] + curr_time[:4])
        #                     DAY             MONTH            YEAR
        day_temp.append(data['hourly']['temperature_2m'][i * DAY + MORNING])
        night_temp.append(data['hourly']['temperature_2m'][i * DAY + NIGHT])
    return {'date': dates,
            'day_temp': day_temp,
            'night_temp': night_temp,
            'humidity': avg_humidity,
            'location': geo_data['location']
            }
