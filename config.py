# config.py
import os
from dotenv import load_dotenv

load_dotenv()

def env(name, default=None, required=False):
    v = os.getenv(name, default)
    if required and (v is None or v == ""):
        raise RuntimeError(f"Missing env var: {name}")
    return v

DB_USER = env('DB_USER', 'caruser')
DB_PASSWORD = env('DB_PASSWORD', 'StrongPass123')
DB_HOST = env('DB_HOST', '127.0.0.1')   # Docker Compose'da 'db' olabilir
DB_PORT = env('DB_PORT', '5432')
DB_NAME = env('DB_NAME', 'cardb')
SECRET_KEY = env('SECRET_KEY', 'dev-secret')

# ÖNEMLİ: Eğer dışarıdan SQLALCHEMY_DATABASE_URI verilmişse onu kullan.
# (K8s demo modunda SQLite kullanacağız)
SQLALCHEMY_DATABASE_URI = os.getenv(
    'SQLALCHEMY_DATABASE_URI',
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

SQLALCHEMY_TRACK_MODIFICATIONS = False
