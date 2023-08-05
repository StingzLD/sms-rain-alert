import requests

# Website to find your Latitude and Longitude:
#   https://www.latlong.net/
# Website used to find a location where it is currently raining:
#   https://www.ventusky.com/
# Weather condition codes:
#   https://openweathermap.org/weather-conditions#Weather-Condition-Codes-2

owm_endpoint = "https://api.openweathermap.org/data/3.0/onecall"
api_key = "87b297d28dca77fa42dc81c9ea35dcca"

weather_params = {
    "lat": "45.151",
    "lon": "-98.413",
    "appid": api_key,
    "units": "imperial",
    "exclude": "current,minutely,daily"
}

response = requests.get(owm_endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()
hourly_data = weather_data['hourly'][:12]  # Next 12 hours

for hour in hourly_data:
    condition_code = hour['weather'][0]['id']
    if int(condition_code) < 600:  # If it is raining
        print("Bring an umbrella")
        break
