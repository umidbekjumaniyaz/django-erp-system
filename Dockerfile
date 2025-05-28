FROM python:3.11-slim

# Django muhit sozlamalari
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Kutubxonalarni o‘rnatish
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Loyihani konteynerga ko‘chirish
COPY . .

# Gunicorn orqali ishga tushurish
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
