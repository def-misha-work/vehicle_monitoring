# Используем официальный Python образ
FROM python:3.11-slim

# Устанавливаем зависимости не python
RUN apt-get update && apt-get install -y make gcc htop

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY ./requirements.txt /app/requirements.txt
COPY ./ /app/

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Открываем порт 8080
EXPOSE 8080

# Команда для запуска приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
