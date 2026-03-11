import requests
from app.schemas.weather import WeatherResponse, WeatherResult
from app.database import init_db
from app.database import SessionLocal
from app.models.weather import WeatherRequest
from datetime import datetime, timedelta, timezone
from app.services.analytics import get_city_stats


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
   db = SessionLocal()
   try:
      # 1. Ищем последнюю запись для этого города в базе
      last_entry = db.query(WeatherRequest).filter(
      WeatherRequest.city == data.city.title()
      ).order_by(WeatherRequest.created_at.desc()).first()

      # 2. Проверяем, насколько она свежая
      if last_entry:
         # Вычисляем разницу между "сейчас" и временем записи в базе
         # Убедись, что оба значения либо с таймзоной, либо без (для SQLite обычно без)
         time_diff = datetime.now(timezone.utc) - last_entry.created_at.replace(tzinfo=timezone.utc)
         if time_diff < timedelta(minutes=10):
            print(f"⏳ Данные для {data.city} еще свежие (обновлено {time_diff.seconds // 60} мин. назад). Пропускаем сохранение.")
            return

      # 3. Если записи нет или она старая — сохраняем
      new_entry = WeatherRequest(
      city=data.city.title(),
      temperature=data.temperature_c,
      wind_speed=data.wind_speed
      )
      db.add(new_entry)
      db.commit()
      print(f"✅ Данные для города {data.city} успешно сохранены в БД.")
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
               print(f"Минимальная температура: {stats['min_temperature']}°C")
               print(f"Максимальная температура: {stats['max_temperature']}°C")
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