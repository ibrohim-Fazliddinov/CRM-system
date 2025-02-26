# Базовый образ
FROM python:3.11

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY . .

# Открываем порт для сервера
EXPOSE 8000

# Команда по умолчанию
CMD ["gunicorn", "your_project.wsgi:application", "--bind", "0.0.0.0:8000"]
