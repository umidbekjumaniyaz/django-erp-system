# Python bazasidan boshlaymiz
FROM python:3.11-slim

# Ishchi katalog yaratamiz
WORKDIR /app

# Talablar faylini ko‘chiramiz va o‘rnatamiz
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Loyihani konteynerga ko‘chiramiz
COPY . .

# Port ochamiz
EXPOSE 8000

# Gunicorn orqali loyihani ishga tushiramiz
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]