from sqlalchemy import func
from app.database import SessionLocal
from app.models.weather import WeatherRequest

def get_city_stats(city_name: str):
   db = SessionLocal()
   try:
      stats = db.query(
         func.avg(WeatherRequest.temperature).label("avg_temp"),
         func.min(WeatherRequest.temperature).label("min_temperature"),
         func.max(WeatherRequest.temperature).label("max_temperature"),
         func.max(WeatherRequest.wind_speed).label("max_wind"),
         func.count(WeatherRequest.id).label("total_records")
      ).filter(WeatherRequest.city == city_name.title()).first()
      
      if not stats or stats.total_records == 0:
         return None
            
      return {
         "city": city_name.title(),
         "avg_temp": round(stats.avg_temp, 1),
         "min_temperature": stats.min_temperature,
         "max_temperature": stats.max_temperature,
         "max_wind": stats.max_wind,
         "count": stats.total_records
      }
   finally:
      db.close()