import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://weather_user:weather_pass@localhost:5432/weather_db"
)