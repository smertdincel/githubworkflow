FROM python:3.11-slim

# psycopg2 ve benzeri paketler için gerekliler
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama kodu
COPY . .

# Üretim portu
ENV PORT=8080
EXPOSE 8080

# Loglar doğrudan stdout
ENV PYTHONUNBUFFERED=1

# Gunicorn ile çalıştır (app.py içindeki 'app' objesi)
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8080", "app:app"]
