import enum
from sqlalchemy import Column, Integer, String, Float, Date, Time, Enum
from sqlalchemy.orm import relationship
from .base import Base

class WindDirectionEnum(str, enum.Enum):
    N   = "N";   NNE = "NNE"; NE  = "NE";  ENE = "ENE"
    E   = "E";   ESE = "ESE"; SE  = "SE";  SSE = "SSE"
    S   = "S";   SSW = "SSW"; SW  = "SW";  WSW = "WSW"
    W   = "W";   WNW = "WNW"; NW  = "NW";  NNW = "NNW"

class WeatherRecord(Base):
    __tablename__ = "weather_records"

    id             = Column(Integer, primary_key=True, autoincrement=True)
    country        = Column(String(100), nullable=False)
    location_name  = Column(String(150))
    last_updated   = Column(Date, nullable=False)
    last_updated_time = Column(Time) 
    wind_kph       = Column(Float)
    wind_degree    = Column(Integer)
    wind_direction = Column(Enum(WindDirectionEnum))
    temperature_c  = Column(Float)
    humidity       = Column(Integer)
    condition_text = Column(String(255))

    celestial = relationship(
        "CelestialEvents",
        back_populates="weather",
        uselist=False,
        cascade="all, delete-orphan"
    )