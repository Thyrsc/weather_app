import requests
from app.schemas.weather import WeatherResponse, WeatherResult
from app.database import init_db
from app.database import SessionLocal
from app.models.weather import WeatherRequest
from datetime import datetime, timedelta, timezone
from app.services.analytics import get_city_stats
from app.models.weather import City, WeatherRequest
from app.database import SessionLocal

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
   save_weather_to_db(result.city, result.temperature_c, result.wind_speed)
   print(f"В городе {city_name} сейчас {current_weather.temperature}°C")
   return result

def save_weather_to_db(city_name: str, temp: float, wind: float):
   db = SessionLocal()
   try:
      # 1. Ищем город в таблице City
      city = db.query(City).filter(City.name == city_name.title()).first()
      
      # 2. Если города нет, создаем его
      if not city:
         city = City(name=city_name.title())
         db.add(city)
         db.commit()
         db.refresh(city) # Теперь у нас есть city.id
      
      # 3. Создаем запись погоды, используя ID города
      new_record = WeatherRequest(
         
         city_id=city.id,
         temperature=temp,
         wind_speed=wind
      )
      db.add(new_record)
      db.commit()
      print(f"✅ Данные для города {city.name} (ID: {city.id}) успешно сохранены.")
      
   except Exception as e:
      print(f"❌ Ошибка при работе с БД: {e}")
      db.rollback()
   finally:
      db.close()

if __name__ == "__main__":
   print("🌤️ Добро пожаловать в Weather App!")
   init_db()
   while True:
      print("\nВведите название города на английском (или 'exit' для выхода):")
      city_name = input(">> ").strip()
      
      # Проверяем, хочет ли пользователь выйти
      if city_name.lower() in ['exit', 'quit', 'выход']:
         print("👋 До свидания!")
         break
      if not city_name:
         continue
      if city_name.lower() == 'stats':
            target_city = input("Для какого города показать статистику? ")
            stats = get_city_stats(target_city)
            if stats:
               print(f"\n--- Статистика по городу {stats['city']} ---")
               print(f"Всего записей: {stats['count']}")
               print(f"Средняя температура: {stats['avg_temp']}°C")
               print(f"Минимальная температура: {stats['min_temp']}°C")
               print(f"Максимальная температура: {stats['max_temp']}°C")
               print(f"Максимальный ветер: {stats['max_wind']} м/с")
            else:
               print("Данных по этому городу пока нет.")
            continue
      # Запускаем нашу логику
      result = get_weather_for_city(city_name)
      
      if result:
         print(f"📊 Данные успешно обработаны для: {result.city}")
      else:
         print(f"❌ Не удалось найти город '{city_name}'. Попробуйте еще раз.")