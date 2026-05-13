from sqlalchemy import Column, Integer, String, Float
from database import Base

class ImpactsEurope(Base):
    __tablename__ = "impacts_europe"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    crater_name = Column(String)
    location = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    diameter_km = Column(Float)
    age_million_years = Column(Float)
    exposed = Column(String)
    drilled = Column(String)
    target_rock = Column(String)
    bolide_type = Column(String)



