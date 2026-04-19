import sys
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URL
from models.base import Base
from models.weather import WeatherRecord
from models.celestial_events import CelestialEvents
from repositories.weather_repository import WeatherRepository
from services.weather_service import WeatherService
from services.etl_service import load_csv

engine  = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)

def show_menu():
    print("\n╔══════════════════════════════╗")
    print("║          Weather DB          ║")
    print("╠══════════════════════════════╣")
    print("║  1. Завантажити дані з CSV   ║")
    print("║  2. Пошук за країною/датою   ║")
    print("║  3. Вийти                    ║")
    print("╚══════════════════════════════╝")

def main():
    with Session() as session:
        repo    = WeatherRepository(session)
        service = WeatherService(repo)

        while True:
            show_menu()
            choice = input("Оберіть опцію: ").strip()

            if choice == "1":
                load_csv(session, "data/GlobalWeatherRepository.csv")

            elif choice == "2":
                country  = input("Країна (англ., напр. Ukraine): ").strip()
                date_str = input("Дата (РРРР-ММ-ДД, напр. 2023-03-15): ").strip()
                try:
                    query_date = date.fromisoformat(date_str)
                except ValueError:
                    print("Невірний формат дати! Використовуйте РРРР-ММ-ДД")
                    continue

                results = service.get_weather_info(country, query_date)
                if not results:
                    print(f"\nЗаписів для '{country}' на {date_str} не знайдено.")
                    continue

                for r in results:
                    w = r["weather"]
                    c = r["celestial"]
                    time_str = f" {w.last_updated_time}" if w.last_updated_time else ""
                    print(f"\n{'─'*50}")
                    print(f"📍 {w.location_name}, {w.country}  |  {w.last_updated}{time_str}")
                    print(f"{'─'*50}")
                    print(f"  🌡️  Температура  : {w.temperature_c} °C")
                    print(f"  💧 Вологість    : {w.humidity} %")
                    print(f"  🌤️  Стан         : {w.condition_text}")
                    wind_dir = w.wind_direction.value if w.wind_direction else "—"
                    print(f"  💨 Вітер        : {w.wind_kph} км/г, {wind_dir} ({w.wind_degree}°)")
                    if c:
                        print(f"  🌅 Схід сонця  : {c.sunrise}   🌇 Захід: {c.sunset}")
                        print(f"  🌕 Схід місяця : {c.moonrise}  🌑 Захід: {c.moonset}")
                        print(f"  🌙 Фаза місяця : {c.moon_phase} ({c.moon_illumination}%)")
                        ans = "✅ Так, варто виходити!" if c.go_outside else "❌ Краще залишитися вдома"
                        print(f"  🚶 Виходити?   : {ans}")

            elif choice == "3":
                print("Завершення програми")
                break

            else:
                print(f"Невідома опція '{choice}'. Введіть 1, 2 або 3.")

if __name__ == "__main__":
    main()