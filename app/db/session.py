import os
from sqlalchemy import create_all, create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv() # Загружаем переменные из .env

# Берем URL базы из настроек (мы их пропишем в .env позже)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://weather_user:weather_pass@db:5432/weather_app")

# Создаем движок
engine = create_engine(DATABASE_URL)

# Создаем фабрику сессий (наш инструмент для работы с БД)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
   """Функция для получения сессии базы данных"""
   db = SessionLocal()
   try:
      yield db
   finally:
      db.close()