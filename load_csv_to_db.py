import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import ImpactsEurope  # Používáme váš SQLAlchemy model

# Vytvoření připojení k databázi
DATABASE_URL = "sqlite:///impacts_europe.db"
engine = create_engine(DATABASE_URL)

# Funkce pro načtení CSV do SQLite
def load_csv_to_db(csv_file):
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        with Session(engine) as session:
            for row in reader:
                # Přidání záznamů z CSV do SQLAlchemy modelu
                new_crater = ImpactsEurope(
                    crater_name=row['crater_name'],
                    location=row['location'],
                    diameter_km=row['diameter_km'],
                )
                session.add(new_crater)
            session.commit()
            print(f"✅ Načteno {session.query(ImpactsEurope).count()} záznamů z {csv_file} do databáze.")

# Načtení dat z CSV do databáze
load_csv_to_db("impacts_europe.csv")
