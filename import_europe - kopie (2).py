import csv
from sqlalchemy.orm import Session
from database import SessionLocal, ImpactsEurope

def import_european_craters():
    db: Session = SessionLocal()

    with open("impacts_europe.csv", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Kontrola existence podle crater_name
            existing = db.query(ImpactsEurope).filter(ImpactsEurope.crater_name == row["crater_name"]).first()
            if not existing:
                new_crater = ImpactsEurope(
                    crater_name=row["crater_name"],
                    location=row["location"],
                    latitude=float(row["latitude"]) if row["latitude"] else 0.0,
                    longitude=float(row["longitude"]) if row["longitude"] else 0.0,
                    diameter_km=float(row["diameter_km"]) if row["diameter_km"] else 0.0,
                    age_million_years=float(row["age_million_years"]) if row["age_million_years"] else 0.0,
                    exposed=row["exposed"],
                    drilled=row["drilled"],
                    target_rock=row["target_rock"],
                    bolide_type=row["bolide_type"]
                )
                db.add(new_crater)

    db.commit()
    db.close()
    print("✅ Import dokončen.")

if __name__ == "__main__":
    import_european_craters()