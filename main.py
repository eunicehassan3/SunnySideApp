import requests
import os
import json
import urllib.parse

# KEY = os.environ.get('TOMORROW_KEY')
# LOCATION = '60448 US'
# TIMESTEPS = '1d'
# UNITS = 'imperial'

# url = f"https://api.tomorrow.io/v4/weather/forecast?location={LOCATION}&timesteps={TIMESTEPS}&units={UNITS}&apikey={KEY}"

# headers = {"accept": "application/json"}

# response = requests.get(url, headers=headers)
# response_data = json.loads(response.text)

# formatted_response = json.dumps(response_data, indent=4)
# print(formatted_response)


def readCity():
      city = input("Please enter the name of your city: ")
      location = urllib.parse.quote(city)
      return location


# temperatureMax
# temperatureMin
# UVIndex
# Visibility
# rainAccumulationAvg
# windSpeedMax
# WindSpeedMin
# WindSpeedAvg
