import os
import requests
from twilio.rest import Client

# Sensible data is stored in environment variables.
# Setting Open Weather API:
open_weather_appid = os.environ.get("OPEN_WEATHER_APPID")
params = {
    "lat": 42.697708,
    "lon": 23.321867,
    "exclude": "current,minutely,daily,alerts",
    "appid": open_weather_appid,
    "units": "metric"
}
endpoint = "https://api.openweathermap.org/data/2.5/onecall"
response = requests.get(endpoint, params)
response.raise_for_status()
data = response.json()

# Setting Twilio API:
twilio_id = os.environ.get("TWILIO_ID")
twilio_auth = os.environ.get("TWILIO_AUTH")
client = Client(twilio_id, twilio_auth)

# If first 12 hours of the day have any type of rain or snow, send an SMS:
weather_first_12_hours = [hour["weather"][0]["id"] for hour in data["hourly"][0:12]]
for _ in weather_first_12_hours:
    if _ < 700:
        message = client.messages.create(from_=os.environ.get("SENDER_PHONE"), to=os.environ.get("RECEIVER_PHONE"),
                                         body="Weather conditions will require an umbrella!")
        break
