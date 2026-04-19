from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.weather import WeatherRecord
from models.celestial_events import CelestialEvents
from datetime import date

class WeatherRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_country_and_date(self, country: str, query_date: date):
        return (
            self.session.query(WeatherRecord)
            .filter(
                and_(
                    WeatherRecord.country.ilike(f"%{country}%"),
                    WeatherRecord.last_updated == query_date,
                )
            )
            .all()
        )

    def get_celestial_by_weather_id(self, weather_id: int):
        return (
            self.session.query(CelestialEvents)
            .filter(CelestialEvents.weather_id == weather_id)
            .first()
        )