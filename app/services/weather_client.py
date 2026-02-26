import requests  # Мы берем в руки "телефон"

def get_weather_for_city(city_name):
   geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json"
   
   geo_response = requests.get(geo_url)
   
   geo_data = geo_response.json()
   
   first_city = geo_data["results"][0]
   
   latitude = first_city["latitude"]
   longitude = first_city["longitude"]   
   
   url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
   
   response = requests.get(url)
   
   data = response.json()
   
   current = data["current_weather"]
   temperature = current["temperature"]
   wind = current["windspeed"]
   
   print(f"В городе {city_name} сейчас: {temperature} градусов.")
   print(f"Скорость ветра: {wind} км/ч.")
   
   return {
      "city": city_name,
      "temperature_c": temperature,
      "wind_speed": wind
   }

get_weather_for_city('Minsk')