from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# Базовый класс, от которого будут наследоваться все наши таблицы
Base = declarative_base()

class WeatherRequest(Base):
   __tablename__ = 'weather_requests'

   id = Column(Integer, primary_key=True)
   city = Column(String, nullable=False) # Город (не может быть пустым)
   temperature_c = Column(Float)         # Температура
   description = Column(String)         # Описание (облачно и т.д.)
   humidity = Column(Integer, nullable=True)
   wind_speed = Column(Float, nullable=True)
   source = Column(String)              # Какой API использовали
   requested_at = Column(DateTime)      # Время запроса
   created_at = Column(DateTime, default=datetime.utcnow) # Когда запись попала в базу

   def __repr__(self):
      return f"<WeatherRequest(city='{self.city}', temp={self.temperature_c})>"