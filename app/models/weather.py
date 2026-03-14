from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base  # Это правильно


class City(Base):
   __tablename__ = "cities"
   
   id = Column(Integer, primary_key=True, index=True)
   name = Column(String, unique=True, nullable=False)
   
   # Связь с записями погоды
   weather_records = relationship("WeatherRequest", back_populates="city_rel")

class WeatherRequest(Base):
   __tablename__ = "weather_requests"

   id = Column(Integer, primary_key=True, index=True)
   
   # Указываем на ID города. ForeignKey теперь импортирован!
   city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
   
   temperature = Column(Float)
   wind_speed = Column(Float)
   created_at = Column(DateTime(timezone=True), server_default=func.now())

   # Обратная связь к объекту City
   city_rel = relationship("City", back_populates="weather_records")