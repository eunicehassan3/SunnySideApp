import requests
import os
import json
import urllib.parse
import datetime
import sqlalchemy as db
import pandas as pd
import sqlite3

KEY = os.environ.get('TOMORROW_KEY')


def prompt():

    print('Z = Zip Code')
    print('C = City Name')
    print('S = Select Existing City from DataBase')
    location = input(
        'How would you like to get your weather information? ')
    if location == 'Z':
        return readZip()
    elif location == 'C':
        return readCity()
    elif location == 'S':
        return chooseData()
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


def chooseData():
    engine = db.create_engine('sqlite:///cities.db')
    try:
        with engine.connect() as connection:
            query_result = connection.execute(
                db.text("SELECT * FROM locationData;")
            ).fetchall()
            stored_locations = pd.DataFrame(query_result)

        stored_locations['name'] = stored_locations['name'].str.split(
            ',', n=1
        ).str[0]
        print("Stored Locations:")
        print(stored_locations)
        selection = input(
            "Enter the number of the location you want to choose: "
        )
        if selection.isdigit():
            selection = int(selection)
            if 0 <= selection < len(stored_locations):
                location = stored_locations.loc[selection, 'name']
                return location
            else:
                print("Invalid selection")
        else:
            print("Invalid input")

        return chooseData()
    # Catch statement for if the database doesnt exist
    except db.exc.OperationalError:
        print("Table does not yet exist, try entering data first")
        return prompt()


def command(location):
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


def realTime(location):
    url = (
        f"https://api.tomorrow.io/v4/weather/"
        f"realtime?location={location}&units=imperial&apikey={KEY}"
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
    print()
    cityToDb(response_data['location'])


def hourly(location):
    url = (
        f"https://api.tomorrow.io/v4/weather/forecast"
        f"?location={location}&timesteps=1h&units=imperial&apikey={KEY}"
    )
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    response_data = json.loads(response.text)
    loc = response_data["location"]["name"]
    forecasts = response_data["timelines"]["hourly"]
    print("Hourly forecast in ", loc)
    print()
    for forecast in forecasts[:24]:
        time = format_time(forecast["time"])
        vals = forecast["values"]
        temp = vals["temperature"]
        condition = get_weather_condition(vals["weatherCode"])
        print(time)
        print("Temperature:", temp, "F")
        print("It is expected to be", condition)
        print()
    cityToDb(response_data['location'])


def nextFive(location):
    url = (
        f"https://api.tomorrow.io/v4/weather/forecast?"
        f"location={location}&timesteps=1d&units=imperial&apikey={KEY}"
    )
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    response_data = json.loads(response.text)
    loc = response_data["location"]["name"]
    print("Weekly Forecast for", loc)
    print()
    forecasts = response_data["timelines"]["daily"]
    for days in forecasts:
        wkday = date_to_day(days["time"])
        avgTemp = days["values"]["temperatureAvg"]
        minTemp = days["values"]["temperatureMin"]
        maxTemp = days["values"]["temperatureMax"]
        condition = get_weather_condition(days["values"]["weatherCodeMax"])
        print("Day:", wkday)
        print("It is forecasted to be", condition)
        print("Average Temperature:", avgTemp, "F")
        print("The low for the day is:", minTemp, "F")
        print("The high for the day is:", maxTemp, "F")
        print()
    cityToDb(response_data['location'])


def date_to_day(date):
    try:
        date_obj = datetime.datetime.strptime(date, "%Y-%m-%dT00:00:00Z")
        day_of_week = date_obj.strftime("%A")
        return day_of_week
    except ValueError:
        return "Invalid date format. Please use YYYY-MM-DD."


def format_time(time):
    time_utc = datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')
    cst_offset = datetime.timedelta(hours=-5)
    time_cst = time_utc + cst_offset
    time_formatted = time_cst.strftime('%Y-%m-%d %H:%M:%S')
    return time_formatted


def cityToDb(locationData):
    df = pd.DataFrame.from_dict([locationData])
    engine = db.create_engine('sqlite:///cities.db')
    try:
        with engine.connect() as connection:
            query = db.text("SELECT * FROM locationData WHERE name=:name;")
            existing_data = connection.execute(
                query, {'name': locationData['name']}
            ).fetchall()
            # This means it wasn't found in the db
            if len(existing_data) == 0:
                # Insert new location
                df.to_sql(
                    'locationData',
                    con=engine,
                    if_exists='append',
                    index=False
                )
                print("Location added successfully!")
                print()
            else:
                print("Location already exists in the table.")
                print()
    # This will run if the DB doesnt exist yet
    except db.exc.OperationalError:
        with engine.connect() as connection:
            df.to_sql(
                'locationData',
                con=engine,
                if_exists='append',
                index=False
            )
            print("Location added successfully!")
            print()


def main():
    location = prompt()
    command(location)


if __name__ == "__main__":
    main()
