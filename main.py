import requests
import os
from twilio.rest import Client

# Website to find your Latitude and Longitude:
#   https://www.latlong.net/
# Website used to find a location where it is currently raining:
#   https://www.ventusky.com/
# Weather condition codes:
#   https://openweathermap.org/weather-conditions#Weather-Condition-Codes-2

owm_endpoint = "https://api.openweathermap.org/data/3.0/onecall"
owm_api_key = os.environ['OWM_API_KEY']
twilio_account_sid = os.environ['TWILIO_ACCOUNT_SID']
twilio_auth_token = os.environ['TWILIO_AUTH_TOKEN']

weather_params = {
    "lat": os.environ['MY_HOME_LATITUDE'],
    "lon": os.environ['MY_HOME_LONGITUDE'],
    "appid": owm_api_key,
    "units": "imperial",
    "exclude": "current,minutely,daily"
}

response = requests.get(owm_endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()
hourly_data = weather_data['hourly'][:12]  # Next 12 hours

will_rain = False

for hour in hourly_data:
    condition_code = hour['weather'][0]['id']
    if int(condition_code) < 600:  # If it is raining
        will_rain = True
        break

if will_rain:
    client = Client(twilio_account_sid, twilio_auth_token)

    message = client.messages \
        .create(
            body="🌧️ Rain is in today's forecast. 🌧️\n☔ Bring an umbrella. ☔",
            from_=os.environ['MY_TWILIO_NUMBER'],
            to=os.environ['MY_PHONE_NUMBER']
        )
    print(message.status)
else:
    print("No rain in the forecast")
