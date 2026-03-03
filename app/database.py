from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.weather import Base
from sqlalchemy.orm import Session

# Путь к файлу базы данных SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./weather.db"

# Создаем "движок" - он отвечает за само соединение
engine = create_engine(
   SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Сессия - это наш "канал" для отправки запросов в базу
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
   """Функция для создания таблиц."""
   # Берет все чертежи из Base и создает их в файле weather.db
   Base.metadata.create_all(bind=engine)

def get_db():
   """Создает новую сессию базы данных и гарантирует её закрытие."""
   db = SessionLocal()
   try:
      yield db
   finally:
      db.close()