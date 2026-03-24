# 1. Используем легкий образ Python
FROM python:3.11-slim

# 2. Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# 3. Копируем файл зависимостей
COPY requirements.txt .

# 4. Устанавливаем библиотеки (без кэша, чтобы образ был меньше)
RUN pip install --no-cache-dir -r requirements.txt

# 5. Копируем всё остальное (папку app и main.py)
COPY . .

# 6. Открываем порт 8000
EXPOSE 8000

# 7. Команда для запуска сервера
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]