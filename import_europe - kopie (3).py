import csv
import re
from sqlalchemy.orm import Session
from database import SessionLocal, ImpactsEurope

def clean_coord(coord_str):
    if not coord_str:
        return 0.0
    # Odstraní písmena N, S, E, W, stupně, minuty a mezery
    clean = re.sub(r'[NSWE°\'\s]', '', coord_str)
    try:
        return float(clean)
    except ValueError:
        return 0.0

def import_european_craters():
    db: Session = SessionLocal()
    try:
        with open("impacts_europe.csv", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                existing = db.query(ImpactsEurope).filter(ImpactsEurope.crater_name == row["crater_name"]).first()
                if not existing:
                    new_crater = ImpactsEurope(
                        crater_name=row["crater_name"],
                        location=row["location"],
                        latitude=clean_coord(row["latitude"]),
                        longitude=clean_coord(row["longitude"]),
                        diameter_km=float(row["diameter_km"]) if row["diameter_km"] else 0.0,
                        age_million_years=float(row["age_million_years"]) if row["age_million_years"] else 0.0,
                        exposed=row["exposed"],
                        drilled=row["drilled"],
                        target_rock=row["target_rock"],
                        bolide_type=row["bolide_type"]
                    )
                    db.add(new_crater)
        db.commit()
        print("✅ Import dokončen.")
    except Exception as e:
        print(f"❌ Chyba při importu: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    import_european_craters()