import requests
import os
import json
import urllib.parse

# KEY = os.environ.get('TOMORROW_KEY')
# LOCATION = '60448 US'
# TIMESTEPS = '1d'
# UNITS = 'imperial'

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

            
# temperatureMax
# temperatureMin
# UVIndex
# Visibility
# rainAccumulationAvg
# windSpeedMax
# WindSpeedMin
# WindSpeedAvg
