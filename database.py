import os
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Získání absolutní cesty k adresáři, kde se nachází tento soubor
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "impacts_europe.db")
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class ImpactsEurope(Base):
    __tablename__ = "impacts_europe"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    crater_name = Column(String, index=True)
    location = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    diameter_km = Column(Float)
    age_million_years = Column(Float)
    exposed = Column(String)
    drilled = Column(String)
    target_rock = Column(String)
    bolide_type = Column(String)

Base.metadata.create_all(bind=engine)