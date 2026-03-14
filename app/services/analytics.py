from sqlalchemy import func
from app.database import SessionLocal
from app.models.weather import City, WeatherRequest

def get_city_stats(city_name: str):
   db = SessionLocal()
   try:
      # Соединяем таблицы City и WeatherRequest по общему ID
      stats = db.query(
         func.avg(WeatherRequest.temperature).label("avg_temp"),
         func.min(WeatherRequest.temperature).label("min_temp"),
         func.max(WeatherRequest.temperature).label("max_temp"),
         func.max(WeatherRequest.wind_speed).label("max_wind"),
         func.count(WeatherRequest.id).label("total_records")
      ).join(City).filter(City.name == city_name.title()).first()
      
      if not stats or stats.total_records == 0:
         return None
         
      return {
         "city": city_name.title(),
         "avg_temp": round(stats.avg_temp, 1),
         "min_temp": stats.min_temp,
         "max_temp": stats.max_temp,
         "max_wind": stats.max_wind,
         "count": stats.total_records
      }
   finally:
      db.close()