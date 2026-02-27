import requests

# КОРОБКА 1: Поиск координат (Геокодирование)
def _get_coordinates(city_name):
   """Ищет широту и долготу по названию города."""                
   geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json"
   geo_response = requests.get(geo_url)
   geo_data = geo_response.json()

   if "results" not in geo_data:
      print(f"Город {city_name} не найден.")
      return None, None

   first_result = geo_data["results"][0]
   return first_result["latitude"], first_result["longitude"]

# КОРОБКА 2: Получение погоды по координатам
def _get_weather_data(lat, lon):
   """Делает запрос к API погоды по координатам."""
   url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
   response = requests.get(url)
   return response.json()

# КОРОБКА 3: Главная (Основная логика)
def get_weather_for_city(city_name):
   """Главная функция: собирает всё вместе и отдает результат."""
   # 1. Сначала узнаем координаты
   lat, lon = _get_coordinates(city_name)
   
   # Если город не нашли, дальше идти нет смысла
   if lat is None:
      return None

   # 2. Потом узнаем погоду
   data = _get_weather_data(lat, lon)
   current = data["current_weather"]

   # 3. Выводим результат
   temperature = current["temperature"]
   wind = current["windspeed"]
   print(f"В городе {city_name} сейчас {temperature}°C, ветер {wind} км/ч.")
   
   return {
      "city": city_name,
      "temperature_c": temperature,
      "wind_speed": wind
   }

get_weather_for_city('Moscow')