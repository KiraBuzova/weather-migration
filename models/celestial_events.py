from sqlalchemy import Column, Integer, Time, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class CelestialEvents(Base):
    __tablename__ = "celestial_events"

    id                = Column(Integer, primary_key=True, autoincrement=True)
    weather_id        = Column(Integer, ForeignKey("weather_records.id"), nullable=False)
    sunrise           = Column(Time)
    sunset            = Column(Time)
    moonrise          = Column(Time)
    moonset           = Column(Time)
    moon_phase        = Column(String(50))
    moon_illumination = Column(Float)
    go_outside        = Column(Boolean, default=False)

    weather = relationship("WeatherRecord", back_populates="celestial")