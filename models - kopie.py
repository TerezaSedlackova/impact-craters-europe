from sqlalchemy import Column, Integer, String, Float
from database import Base

class ImpactsEurope(Base):
    __tablename__ = "impacts_europe"
    __table_args__ = {"extend_existing": True}

    #id = Column(Integer, primary_key=True, index=True)
    crater_name = Column(String)  # Crater Name (Opraven název proměnné)
    location = Column(String)  # Location (Opraven na správný malý název)
    latitude = Column(Float)
    longitude = Column(Float)
    diameter_km = Column(Float)  # Diameter (km)
    age_million_years = Column(Float)  # Age (Ma)
    exposed = Column(String)  # Exposed
    drilled = Column(String)  # Drilled
    target_rock = Column(String)  # Target Rock
    bolide_type = Column(String)  # Bolide Type




