import requests
import os
from twilio.rest import Client

# Website to find your Latitude and Longitude:
#   https://www.latlong.net/
# Website used to find a location where it is currently raining:
#   https://www.ventusky.com/
# Weather condition codes:
#   https://openweathermap.org/weather-conditions#Weather-Condition-Codes-2

OWM_ENDPOINT = "https://api.openweathermap.org/data/3.0/onecall"
OWM_API_KEY = os.environ['OWM_API_KEY']
TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
TWILIO_PHONE_NUMBER = os.environ['TWILIO_PHONE_NUMBER']
TWILIO_VERIFIED_NUMBER = os.environ['TWILIO_VERIFIED_NUMBER']

weather_params = {
    "lat": os.environ['MY_HOME_LATITUDE'],
    "lon": os.environ['MY_HOME_LONGITUDE'],
    "appid": OWM_API_KEY,
    "units": "imperial",
    "exclude": "current,minutely,daily"
}

response = requests.get(OWM_ENDPOINT, params=weather_params)
response.raise_for_status()
weather_data = response.json()
hourly_data = weather_data['hourly'][:12]  # Next 12 hours

will_rain = False

for hour in hourly_data:
    condition_code = hour['weather'][0]['id']
    probability = hour['pop']

    if int(condition_code) < 600 and probability > 0.5:
        will_rain = True
        break

if will_rain:
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    message = client.messages \
        .create(
            body="🌧️ Rain is in today's forecast. 🌧️\n☔ Bring an umbrella. ☔",
            from_=TWILIO_PHONE_NUMBER,
            to=TWILIO_VERIFIED_NUMBER
        )
    print(message.status)
else:
    print("No rain in the forecast")
