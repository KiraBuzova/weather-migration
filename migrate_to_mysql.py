from sqlalchemy import create_engine, text

PG_URL    = "postgresql+psycopg2://weather_user:weather_pass@localhost:5432/weather_db"
MYSQL_URL = "mysql+pymysql://weather_user:weather_pass@localhost:3306/weather_db"

pg_engine    = create_engine(PG_URL)
mysql_engine = create_engine(MYSQL_URL)

def migrate():
    print("Починаємо міграцію даних PostgreSQL → MySQL...")

    with pg_engine.connect() as pg:
        weather_rows   = pg.execute(text("SELECT * FROM weather_records")).fetchall()
        celestial_rows = pg.execute(text("SELECT * FROM celestial_events")).fetchall()

    with mysql_engine.connect() as mysql:
        print(f"Переносимо {len(weather_rows)} записів weather_records...")
        for i, row in enumerate(weather_rows):
            try:
                mysql.execute(
                    text("""INSERT IGNORE INTO weather_records
                            (id, country, location_name, last_updated,
                             last_updated_time, wind_kph, wind_degree,
                             wind_direction, temperature_c, humidity, condition_text)
                            VALUES (:id, :country, :location_name, :last_updated,
                                    :last_updated_time, :wind_kph, :wind_degree,
                                    :wind_direction, :temperature_c, :humidity, :condition_text)"""),
                    dict(row._mapping)
                )
            except Exception as e:
                print(f"Пропущено weather рядок {i}: {e}")

            if i % 5000 == 0 and i > 0:
                mysql.commit()
                print(f"  Перенесено {i} записів...")

        print(f"Переносимо {len(celestial_rows)} записів celestial_events...")
        for i, row in enumerate(celestial_rows):
            try:
                mysql.execute(
                    text("""INSERT IGNORE INTO celestial_events
                            (id, weather_id, sunrise, sunset, moonrise,
                             moonset, moon_phase, moon_illumination, go_outside)
                            VALUES (:id, :weather_id, :sunrise, :sunset, :moonrise,
                                    :moonset, :moon_phase, :moon_illumination, :go_outside)"""),
                    dict(row._mapping)
                )
            except Exception as e:
                print(f"Пропущено celestial рядок {i}: {e}")

            if i % 5000 == 0 and i > 0:
                mysql.commit()
                print(f"  Перенесено {i} записів...")

        mysql.commit()
    print("Міграція на MySQL завершена!")

if __name__ == "__main__":
    migrate()