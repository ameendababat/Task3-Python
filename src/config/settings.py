import os
from dotenv import load_dotenv
from src.config.definitions import ENV_PATH


load_dotenv(ENV_PATH)

# Database settings
DB_DATABASE = os.getenv("DB_DATABASE")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", 5432))
API_PREFIX = os.getenv("API_PREFIX", "/api/service/v1")
DB_URL = os.getenv(
    "DB_URL",
    f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
)