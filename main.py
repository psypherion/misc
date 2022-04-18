from PIL import Image
import urllib.request
from geopy.geocoders import Nominatim
import requests
from warnings import filterwarnings
import matplotlib.pyplot as plt

filterwarnings('ignore')
geolocator = Nominatim(user_agent="WebApp")
city = input("Enter the city: ")
country = ''
country = input("Enter the country: ")
location = geolocator.geocode(city + ", " + country, timeout = None)
latitude = location.latitude
longitude = location.longitude

API_KEY = "adb128fc22d3c9cd2a59e6de845bc96b"
API_END_POINT = "https://api.openweathermap.org/data/2.5/onecall"

# ------------- Weather Parameters -------------------- #
weather_params = {
    "lat":  latitude,
    "lon": longitude,
    "appid": API_KEY
}
# ------------------ Getting The Response ----------------- #
response = requests.get(API_END_POINT, params=weather_params)

response.raise_for_status()

weather_data = response.json()

# ------------------ GETTING THE DATA -------------------------------- #
curr_temp = round(weather_data['current']['temp']) - 273
feels_like = round(weather_data['current']['feels_like']) - 273
wind_speed = weather_data['current']['wind_speed']
desc = weather_data['current']['weather'][0]['description']
icon = weather_data['current']['weather'][0]['icon']
website = "https://openweathermap.org/img/wn/" + icon + "@2x.png"
print(f"Current Temperature: {curr_temp}\n"
      f"Description : {desc}")

image = r"src\img\weather.png"
urllib.request.urlretrieve(website, image)

#--------------Graphical Representation of Weather-------------------#
daily_max_temp = []
daily_min_temp = []
day_no = [i for i in range(0, 8)]
daily = weather_data['daily']
for day in daily:
    daily_max_temp.append(day['temp']['max'])
    daily_min_temp.append(day['temp']['min'])
plt.plot(day_no, daily_max_temp, color='red', marker='o', linestyle='solid')
plt.show()
plt.plot(day_no, daily_min_temp, color='cyan', marker='o', linestyle='solid')
plt.show()