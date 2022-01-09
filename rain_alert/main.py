import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
import os

owm_endpoint = "https://api.openweathermap.org/data/2.5/onecall"
api_key = "22e937c28d8863d8b21ee418adc24837"

account_sid = 'AC3de4876a9308a2f10bff804d6df8cb04'
auth_token = '6f002e57f351e3b79cba401e83d10cb2'

weather_params = {
    "lat": 17.385044,
    "lon": 78.486671,
    "appid": api_key,
    "exclude": "current,minutely,daily"
}

response = requests.get(owm_endpoint, params=weather_params)
response.raise_for_status
weather_data = response.json()
weather_sliced = weather_data["hourly"][:12]

will_rain = False

for hour_data in weather_sliced:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) > 300:
        will_rain = True
if will_rain == True:
    client = Client(account_sid, auth_token)
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    client = Client(account_sid, auth_token, http_client=proxy_client)

    message = client.messages.create(
        body='Hi there!. Clouds',
        from_='+17744841685',
        to='+916005093758'
    )

    print(message.status)
