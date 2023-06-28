import requests
import os
import json
import urllib.parse
import datetime


KEY = os.environ.get('TOMORROW_KEY')
LOCATION = '60448 US'
TIMESTEPS = '1d'
UNITS = 'imperial'


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
    city = input("Please enter the name of your city: ")
    location = urllib.parse.quote(city)
    return location


def readZip():
    while True:
        zip_code = input('Enter the zip code: ')
        try:
            zip_code = int(zip_code)
            if zip_code > 0:
                location = str(zip_code) + ' US'
                return location
                break
            else:
                print("Invalid zip code")
        except ValueError:
                print("Does nothing")


def command(location):
    # asks user to input RW, NH, HF and NFD
    print('RW = Realtime Weather')
    print('HF = Hourly Forecast, next 24 hours')
    print('NFD = Next Five day Forecast')
    loc = input('Enter command: ')
    if loc == 'RW':
        realTime(location)
    elif loc == 'HF':
        hourly(location)
    elif loc == 'NFD':
        nextFive(location)
    else:
        print('Invalid input, try again!')
        print('')
        command(location)


def get_weather_condition(weather_code):
    with open('weather_codes.json') as file:
        data = json.load(file)

    condition = data.get('weatherCode').get(str(weather_code))
    return condition


# Right now the weather in [location][name] is
# [Weathercodetranslated], at a temperature of ["temperature"]
# The UV index is at [uvIndex]
# The wind speed is [windSpeed] MPH
def realTime(l):
    url = (
        f"https://api.tomorrow.io/v4/weather/"
        f"realtime?location={l}&units=imperial&apikey={KEY}"
    )
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    response_data = json.loads(response.text)
    loc = response_data["location"]["name"]
    condition = get_weather_condition(
        response_data["data"]["values"]["weatherCode"])
    temp = response_data["data"]["values"]["temperature"]
    print(
        "Right now the weather in", loc, "is",
        condition, "at a temperature of", temp, "F"
    )


def hourly(l):
    url = (
        f"https://api.tomorrow.io/v4/weather/"
        f"forecast?location={l}&timesteps=1h&units=imperial&apikey={KEY}"
    )
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    response_data = json.loads(response.text)
    loc = response_data["location"]["name"]
    forecasts = response_data["timelines"]["hourly"]
    print("Hourly forecast in ", loc)
    for forecast in forecasts[:24]:
        # Format the time in a more legible way
        time = forecast["time"]
        time_utc = datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')
        cst_offset = datetime.timedelta(hours=-5)
        time_cst = time_utc + cst_offset
        time_formatted = time_cst.strftime('%Y-%m-%d %H:%M:%S')
        vals = forecast["values"]
        temp = vals["temperature"]
        condition = get_weather_condition(vals["weatherCode"])
        print(
            "At", time_formatted, "it is",
            condition, "at a temperature of", temp, "F"
        )


def nextFive(l):
    url = (
        f"https://api.tomorrow.io/v4/weather/"
        f"forecast?location={l}&timesteps=1d&units=imperial&apikey={KEY}"
    )
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    response_data = json.loads(response.text)
    loc = response_data["location"]["name"]
    forecasts = response_data["timelines"]["daily"]
    for days in forecasts:
        wkday = date_to_day(days["time"])
        avgTemp = days["values"]["temperatureAvg"]
        minTemp = days["values"]["temperatureMin"]
        maxTemp = days["values"]["temperatureMax"]
        print(wkday)


def date_to_day(date):
    try:
        date_obj = datetime.datetime.strptime(date, "%Y-%m-%dT00:00:00Z")
        day_of_week = date_obj.strftime("%A")
        return day_of_week
    except ValueError:
        return "Invalid date format. Please use YYYY-MM-DD."
    # formatted_response = json.dumps(response_data, indent=4)
    # print(formatted_response)
    # print(response_data)


# def main():
location = prompt()
command(location)
# hourly('60448 US')
# realTime('63103 US')
# formatted_response = json.dumps(response_data, indent=4)
# print(formatted_response)

# temperatureMax
# temperatureMin
# UVIndex
# Visibility
# rainAccumulationAvg
# windSpeedMax
# WindSpeedMin
# WindSpeedAvg
