from repositories.weather_repository import WeatherRepository
from datetime import date

def should_go_outside(moon_illumination: float,
                      moon_phase: str,
                      wind_kph: float = 0) -> bool:
    if moon_phase == "Full Moon":
        return False
    if moon_illumination >= 80:
        return False
    if wind_kph and wind_kph > 50:
        return False
    return True

class WeatherService:
    def __init__(self, repository: WeatherRepository):
        self.repo = repository

    def get_weather_info(self, country: str, query_date: date):
        records = self.repo.get_by_country_and_date(country, query_date)
        result = []
        for rec in records:
            celestial = self.repo.get_celestial_by_weather_id(rec.id)
            result.append({"weather": rec, "celestial": celestial})
        return result