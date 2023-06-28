import requests
import os
import json

# KEY = os.environ.get('TOMORROW_KEY')\
# LOCATION = '60448 US'
# TIMESTEPS = '1d'
# UNITS = 'imperial'

# url = f"https://api.tomorrow.io/v4/weather/
#     forecast?location={LOCATION}&timesteps={TIMESTEPS}&units={UNITS}&apikey={KEY}"

# headers = {"accept": "application/json"}

# response = requests.get(url, headers=headers)
# response_data = json.loads(response.text)

# formatted_response = json.dumps(response_data, indent=4)
# print(formatted_response)


def prompt():
    location = input(
        'Would you like to input a zip code or a city name? (Z/C) ')
    if location == 'Z':
        return readZip()
    elif location == 'C':
        return readCity()
    else:
        print("Sorry, that didn't work, "
              "make sure you're inputting an appropriate string")
        return prompt()


def readCity():
    # Need to implement, takes in 'C', returns formatted location,
    # having a return value to pass the styling
    location = ""
    return location


def readZip():
    # Need to implement, takes in 'Z', returns formatted zip code
    # having a return value to pass the styling
    location = ""
    return location


# temperatureMax
# temperatureMin
# UVIndex
# Visibility
# rainAccumulationAvg
# windSpeedMax
# WindSpeedMin
# WindSpeedAvg
