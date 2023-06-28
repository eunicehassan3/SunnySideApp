import requests
import os
import json

#KEY = os.environ.get('TOMORROW_KEY')
#LOCATION = '60448 US'
#TIMESTEPS = '1d'
#UNITS = 'imperial'

#url = f"https://api.tomorrow.io/v4/weather/forecast?location={LOCATION}&timesteps={TIMESTEPS}&units={UNITS}&apikey={KEY}"

#headers = {"accept": "application/json"}

#response = requests.get(url, headers=headers)
#response_data = json.loads(response.text)

#formatted_response = json.dumps(response_data, indent=4)
#print(formatted_response)

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
