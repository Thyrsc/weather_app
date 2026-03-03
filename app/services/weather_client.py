import requests
from app.schemas.weather import WeatherResponse, WeatherResult
from app.database import init_db
from app.database import SessionLocal
from app.models.weather import WeatherRequest


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

def _get_weather_data(lat, lon):
   """Делает запрос к API погоды по координатам."""
   url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
   response = requests.get(url)
   return response.json()

def get_weather_for_city(city_name):
   """Основная функция с использованием Pydantic моделей."""
   lat, lon = _get_coordinates(city_name)
   if lat is None:
      return None
   
   data = _get_weather_data(lat, lon)
   
   # Валидация данных через Pydantic
   current_weather = WeatherResponse(**data["current_weather"])
   result = WeatherResult(
      city=city_name,
      temperature_c=current_weather.temperature,
      wind_speed=current_weather.windspeed
   )
   save_weather_to_db(result)
   print(f"В городе {city_name} сейчас {current_weather.temperature}°C")
   return result

def save_weather_to_db(data: WeatherResult):
   """Сохраняет проверенные данные о погоде в базу данных."""
   # 1. Открываем сессию (канал связи)
   db = SessionLocal()
   try:
      # 2. Создаем "строчку" для базы на основе нашего объекта
      new_entry = WeatherRequest(
         city=data.city.title(), # Используем .title() для красоты
         temperature=data.temperature_c,
         wind_speed=data.wind_speed
      )
      # 3. Добавляем и сохраняем
      db.add(new_entry)
      db.commit()
      print(f"✅ Данные для города {data.city} успешно сохранены в БД.")
   except Exception as e:
      print(f"❌ Ошибка при сохранении в БД: {e}")
      db.rollback() # Откатываем изменения, если что-то пошло не так
   finally:
      db.close() # Всегда закрываем сессию

if __name__ == "__main__":
   print("Создаем таблицы в базе данных...")
   init_db()
   city = "Moscow"
   result = get_weather_for_city(city)
   if result:
      print(f"Объект Pydantic успешно создан: {result}")
   else:
      print("Что-то пошло не так.")