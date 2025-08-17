FROM python:3.10-slim

# psycopg2 için sistem paketleri
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Python bağımlılıkları
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt && pip install --no-cache-dir gunicorn

# Uygulama kodları
COPY . .

# Güvenlik: normal kullanıcı
RUN useradd -m appuser
USER appuser

EXPOSE 8080

# Gunicorn ile Flask'ı çalıştır
CMD ["gunicorn", "-w", "3", "-b", "0.0.0.0:8080", "app:app"]
