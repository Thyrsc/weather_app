from app.database import SessionLocal
from app.models.weather import WeatherRequest, City

def check_my_data():
   db = SessionLocal()
   try:
      # Запрашиваем данные: Имя города, температуру и ТО САМОЕ описание
      records = db.query(
         City.name, 
         WeatherRequest.temperature, 
         WeatherRequest.weather_description,
         WeatherRequest.created_at
      ).join(City).order_by(WeatherRequest.id.desc()).limit(5).all()
      
      if not records:
            print("📭 База данных пока пуста. Запусти weather_client.py и введи город!")
            return
      
      print("\n" + "="*50)
      print(f"{'ГОРОД':<15} | {'ТЕМП':<6} | {'ОПИСАНИЕ':<15} | {'ВРЕМЯ'}")
      print("-"*50)
      
      for city, temp, desc, dt in records:
         # Форматируем время для наглядности
         time_str = dt.strftime("%H:%M:%S") if dt else "N/A"
         print(f"{city:<15} | {temp:<6}°C | {str(desc):<15} | {time_str}")
      print("="*50 + "\n")     
   except Exception as e:
      print(f"❌ Ошибка при чтении базы: {e}")
   finally:
      db.close()

if __name__ == "__main__":
   check_my_data()