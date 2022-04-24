from PIL import Image
import urllib.request
from geopy.geocoders import Nominatim
import requests
from warnings import filterwarnings
import matplotlib.pyplot as plt
from datetime import date
filterwarnings('ignore')
import streamlit as st

# -------------- Date-Time ------------------------------#
today = date.today()
d1 = today.strftime("%d/%m/%Y") # dd/mm/YYYY

# --------------- ApI Keys ------------------------------#
API_KEY = "adb128fc22d3c9cd2a59e6de845bc96b"
API_END_POINT = "https://api.openweathermap.org/data/2.5/onecall"

#-------------- Building The APP -----------------#
st.title('Weather App')
st.write("Find Weather Details of your city")

# ----------------- Latitude & Longitude -------------------#
geolocator = Nominatim(user_agent="WebApp")
locality = st.text_input("Enter name of your locality: ")
country = st.text_input("Enter name of your country: ")
def get_weather_data(latitude, longitude):
    # ------------- Weather Parameters -------------------- #
    weather_params = {
        "lat":  latitude,
        "lon": longitude,
        "appid": API_KEY
    }
    # ------------------ Getting The Response ----------------- #
    response = requests.get(API_END_POINT, params=weather_params)
    data = response.json()
    return data

# ------------------ GETTING THE DATA -------------------------------- #
def show_data(weather_data):
    # ------------------ GETTING THE DATA -------------------------------- #
    curr_temp = round(weather_data['current']['temp']) - 273
    feels_like = round(weather_data['current']['feels_like']) - 273
    wind_speed = weather_data['current']['wind_speed']
    desc = weather_data['current']['weather'][0]['description']
    icon = weather_data['current']['weather'][0]['icon']
    humidity = weather_data['current']['humidity']
    return curr_temp, feels_like, wind_speed, desc, humidity

#------------------ Weather Change ----------------------#
def weather_change(weather_slice):
    temp_change = weather_slice[0]['temp'] - weather_data['current']['temp']
    humidity_change = weather_slice[0]['humidity'] - weather_data['current']['humidity']
    windspeed_change = weather_slice[0]['wind_speed'] - weather_data['current']['wind_speed']

    temp_change = round(temp_change, ndigits=2)
    humidity_change = round(humidity_change, ndigits=2)
    windspeed_change = round(windspeed_change, ndigits=2) 
    return temp_change, humidity_change, windspeed_change

# ------- Checking for Rain ---------- #
def rain_checker(weather_slice):
    rain = []
    for hour_data in weather_slice:
        condition = hour_data['weather'][0]['id']
        if int(condition) < 600:
            will_rain = "It's gonna rain today. Take an Umbrella."
            break
        else:
            will_rain = "It's not going to be a rainy day."
    return will_rain


if st.button('Show Weather'):
    if len(locality) > 0:
        location = geolocator.geocode(locality + ", " + country, timeout = None)
        latitude = location.latitude
        longitude = location.longitude
        weather_data = get_weather_data(latitude, longitude)
        weather_slice = weather_data['hourly'][:24]
        curr_temp, feels_like, wind_speed, desc, humidity = show_data(weather_data)
        temp_change, humidity_change, windspeed_change = weather_change(weather_slice)
        rain = rain_checker(weather_slice)
        st.write("Current Temperature: ", curr_temp, "°C")
        st.write("Feels Like: ", feels_like, "°C")
        st.write("Wind Speed: ", wind_speed, "mph")
        st.write("Description: ", desc)
        st.write("Humidity: ", humidity, "%")
        st.write(rain)
        col1, col2, col3= st.columns(3)
        col1.metric("Temperature", curr_temp, f"{temp_change}°C")
        col2.metric("Wind", wind_speed, f"{windspeed_change}mph")
        col3.metric("Humidity", humidity, f"{humidity_change}%")

        icon = weather_data['current']['weather'][0]['icon']    
        website = "https://openweathermap.org/img/wn/" + icon + "@2x.png"
        image = r"src\img\weather.png"
        urllib.request.urlretrieve(website, image)
        st.image(image, width=30)

        #--------------Graphical Representation of Weather-------------------#
        fig = plt.figure(figsize = (10, 5))
        temp_datapoints = [round(i['temp']-273, 2) for i in weather_slice[:24]]
        plt.plot(temp_datapoints)
        plt.title("Temperature Forecast for the next 24 hours")
        plt.xlabel(xlabel="Next 24 Hours")
        plt.ylabel(ylabel="Temperature in Celsius")
        st.pyplot(fig)

        fig = plt.figure(figsize = (10, 5))
        humid_data = [f"{round(i['humidity']/10)*10}" + '%' for i in weather_slice[:24]]
        plt.plot(humid_data)
        plt.title("Humidity Forecast for the next 24 hours")
        plt.xlabel(xlabel="Next 24 Hours")
        plt.ylabel(ylabel="THumidity in %")
        st.pyplot(fig)

        fig = plt.figure(figsize = (10, 5))
        windspeed_datapoints = [round(i['wind_speed'] * 2.23694, 2) for i in weather_slice]
        plt.plot(windspeed_datapoints)
        plt.title("Wind Speed Forecast for the next 24 hours")
        plt.xlabel(xlabel="Next 24 Hours")
        plt.ylabel(ylabel="Wind Speed in Miles per Hour")
        st.pyplot(fig)
else:
    st.write("Please enter the location")
    
#------------------ Weekly Forecasting ----------------------#
if st.button("Weekly Forecast"):
    if len(locality) > 0:
        location = geolocator.geocode(locality + ", " + country, timeout = None)
        latitude = location.latitude
        longitude = location.longitude
        weather_data = get_weather_data(latitude, longitude)
        weather_slice = weather_data['hourly'][:24]
    week_temp = []
    for i in weather_data['daily']:
        each_day = 0
        for j in i['feels_like'].values():
            each_day += j
        avg = each_day/4 - 273
        week_temp.append(avg)
    fig = plt.figure(figsize = (10, 5))
    plt.plot(week_temp)
    plt.title("Weekly Temperature Forecast")
    plt.xlabel(xlabel="Days")
    plt.ylabel(ylabel="Temperature in Celsius")
    st.pyplot(fig)

    fig = plt.figure(figsize = (10, 5))
    week_humid = [f"{round(i['humidity']/10)*10}" for i in weather_data['daily']]
    plt.plot([i for i in range(0, 8)], week_humid, color='green')
    plt.title("Weekly Humidity Forecast")
    plt.xlabel(xlabel="Days")
    plt.ylabel(ylabel="Humidity in %")
    st.pyplot(fig)

    fig = plt.figure(figsize = (10, 5))
    week_wind = [round(i['wind_speed'] * 2.23694, 2) for i in weather_data['daily']]
    plt.plot(week_wind)
    plt.title("Weekly Wind Speed Forecast")
    plt.xlabel(xlabel="Days")
    plt.ylabel(ylabel="Wind Speed in Miles per Hour")
    st.pyplot(fig)