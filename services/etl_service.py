import csv
from datetime import date, datetime
from sqlalchemy.orm import Session
from models.weather import WeatherRecord, WindDirectionEnum
from models.celestial_events import CelestialEvents
from services.weather_service import should_go_outside

def parse_time(val: str):
    if not val or val.strip() == '':
        return None
    for fmt in ('%I:%M %p', '%H:%M'):
        try:
            return datetime.strptime(val.strip(), fmt).time()
        except ValueError:
            continue
    return None

def load_csv(session: Session, filepath: str):
    with open(filepath, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        batch = []
        for i, row in enumerate(reader):
            try:
                wd_raw = row.get('wind_direction', '').strip().upper()
                wind_dir = WindDirectionEnum(wd_raw) \
                    if wd_raw in WindDirectionEnum._value2member_map_ else None

                record = WeatherRecord(
                    country        = row.get('country', ''),
                    location_name  = row.get('location_name', row.get('city', '')),
                    last_updated      = date.fromisoformat(row['last_updated'][:10]),
                    last_updated_time = parse_time(row['last_updated'][11:].strip()) if len(row.get('last_updated','')) > 10 else None,
                    wind_kph       = float(row['wind_kph']) if row.get('wind_kph') else None,
                    wind_degree    = int(float(row['wind_degree'])) if row.get('wind_degree') else None,
                    wind_direction = wind_dir,
                    temperature_c  = float(row['temperature_celsius']) if row.get('temperature_celsius') else None,
                    humidity       = int(float(row['humidity'])) if row.get('humidity') else None,
                    condition_text = row.get('condition_text', ''),
                )
                session.add(record)
                session.flush()

                moon_ill = float(row.get('moon_illumination', 0) or 0)
                moon_ph  = row.get('moon_phase', '').strip()
                wind_kph = float(row.get('wind_kph', 0) or 0)

                celestial = CelestialEvents(
                    weather_id        = record.id,
                    sunrise           = parse_time(row.get('sunrise')),
                    sunset            = parse_time(row.get('sunset')),
                    moonrise          = parse_time(row.get('moonrise')),
                    moonset           = parse_time(row.get('moonset')),
                    moon_phase        = moon_ph,
                    moon_illumination = moon_ill,
                    go_outside        = should_go_outside(moon_ill, moon_ph, wind_kph),
                )
                session.add(celestial)
                batch.append(i)

                # Зберігаємо кожні 500 рядків щоб не навантажувати пам'ять
                if len(batch) >= 500:
                    session.commit()
                    batch = []
                    print(f"  Завантажено {i+1} рядків...")

            except Exception as e:
                print(f"  Пропущено рядок {i}: {e}")
                session.rollback()

        session.commit()
    print("CSV завантажено успішно!")