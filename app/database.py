from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./weather.db"

# Создаем движок
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Фабрика сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()

def init_db():
   # Импортируем модели здесь, чтобы избежать кругового импорта
   import app.models.weather
   # Вот правильный способ вызвать создание таблиц:
   Base.metadata.create_all(bind=engine)

def get_db():
   """Создает новую сессию базы данных и гарантирует её закрытие."""
   db = SessionLocal()
   try:
      yield db
   finally:
      db.close()