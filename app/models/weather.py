from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

# Это родительский класс, который соберет все наши будущие таблицы
Base = declarative_base()

class WeatherRequest(Base):
   """Модель для хранения истории запросов погоды."""
   __tablename__ = "weather_requests"

   id = Column(Integer, primary_key=True, index=True)
   city = Column(String, nullable=False)
   temperature = Column(Float)
   wind_speed = Column(Float)
   
   # Автоматическая дата создания записи
   created_at = Column(DateTime(timezone=True), server_default=func.now())