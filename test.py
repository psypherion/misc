from geopy.geocoders import Nominatim
#Import the required library

# Initialize Nominatim API
geolocator = Nominatim(user_agent="WebApp")

location = geolocator.geocode("Kolkata, India")

print("The latitude of the location is: ", location.latitude)
print("The longitude of the location is: ", location.longitude)
