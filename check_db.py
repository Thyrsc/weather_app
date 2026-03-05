from app.database import SessionLocal
from app.models.weather import WeatherRequest

def view_weather_history():
   # 1. Открываем сессию
   db = SessionLocal()
   try:
      # 2. Запрашиваем все записи из таблицы
      history = db.query(WeatherRequest).all()
      
      if not history:
         print("📭 База данных пока пуста.")
         return
      print(f"{'ID':<4} | {'Город':<15} | {'Темп.':<6} | {'Ветер':<6} | {'Дата'}")
      print("-" * 60)
      
      for entry in history:
         # Форматируем дату для удобства
         date_str = entry.created_at.strftime("%Y-%m-%d %H:%M")
         print(f"{entry.id:<4} | {entry.city:<15} | {entry.temperature:<6}°C | {entry.wind_speed:<6} | {date_str}")
            
   finally:
      db.close()
if __name__ == "__main__":
   view_weather_history()