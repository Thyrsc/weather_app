from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from app.database import init_db
from app.services.weather_client import get_weather_for_city
from app.services.analytics import get_city_stats, get_global_records, get_sunniest_cities

# 1. Создаем функцию жизненного цикла
@asynccontextmanager
async def lifespan(app: FastAPI):
   # Код здесь выполнится ПРИ ЗАПУСКЕ
   print("🚀 Инициализация базы данных...")
   init_db()
   yield
   # Код здесь выполнится ПРИ ВЫКЛЮЧЕНИИ (если нужно что-то закрыть)
   print("🏁 Завершение работы API...")

# 2. Передаем lifespan в FastAPI
app = FastAPI(
   title="Weather Analytics API", 
   version="1.0",
   lifespan=lifespan
)

# Дальше твои эндпоинты @app.get...

@app.get("/")
def read_root():
   return {"message": "Добро пожаловать в Weather API! Перейдите на /docs для тестирования."}

# Эндпоинт для получения погоды (заменяет ввод города в консоли)
@app.get("/weather/{city}")
def fetch_weather(city: str):
   result = get_weather_for_city(city)
   if not result:
      raise HTTPException(status_code=404, detail=f"Город {city} не найден")
   return result

# Эндпоинт для статистики
@app.get("/stats/{city}")
def fetch_stats(city: str):
   stats = get_city_stats(city)
   if not stats:
      raise HTTPException(status_code=404, detail="Данных по этому городу еще нет")
   return stats

# Эндпоинт для всех топов сразу
@app.get("/top")
def fetch_tops():
   return {
      "global_records": get_global_records(),
      "sunniest_cities": get_sunniest_cities()
   }