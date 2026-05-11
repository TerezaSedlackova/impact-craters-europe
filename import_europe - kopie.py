import csv
from sqlalchemy.orm import Session
from database import SessionLocal, ImpactsEurope  # Opravený název modelu

# Funkce pro import dat z CSV (pouze Evropa)
def import_european_craters():
    db: Session = SessionLocal()

    with open("impacts_europe.csv", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Kontrola, zda kráter už existuje v databázi
            existing = db.query(ImpactsEurope).filter(ImpactsEurope.crater_name == row["crater_name"]).first()
            if not existing:
                new_crater = ImpactsEurope(
                    crater_name=row["crater_name"],
                    location=row["location"],
                    diameter_km=float(row["diameter_km"]),
                    age_million_years=float(row["age_million_years"]),
                    exposed=row["exposed"],
                    drilled=row["drilled"],
                    target_rock=row["target_rock"],
                    bolide_type=row["bolide_type"]
                )
                db.add(new_crater)

    db.commit()  # Potvrzení všech změn najednou
    db.close()  # Zavření databázové session
    print("✅ Evropské krátery byly úspěšně importovány!")

# Spuštění importu
if __name__ == "__main__":
    import_european_craters()
