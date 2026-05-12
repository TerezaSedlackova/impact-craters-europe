import csv
import re
from sqlalchemy.orm import Session
from database import SessionLocal, ImpactsEurope

def clean_coord(coord_str):
    if not coord_str or coord_str == "nan":
        return 0.0
    try:
        # Hledá čísla v řetězci (stupně a minuty)
        parts = re.findall(r'\d+', coord_str)
        if len(parts) >= 2:
            degrees = float(parts[0])
            minutes = float(parts[1])
            decimal = degrees + (minutes / 60.0)
            return round(decimal, 4)
        elif len(parts) == 1:
            return float(parts[0])
        return 0.0
    except Exception:
        return 0.0

def import_european_craters():
    db: Session = SessionLocal()
    try:
        with open("impacts_europe.csv", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                lat = clean_coord(row["latitude"])
                lon = clean_coord(row["longitude"])
                
                existing = db.query(ImpactsEurope).filter(ImpactsEurope.crater_name == row["crater_name"]).first()
                
                if existing:
                    # Dočasná aktualizace: přepsání souřadnic u nalezeného záznamu
                    existing.latitude = lat
                    existing.longitude = lon
                else:
                    # Vytvoření nového záznamu, pokud neexistuje
                    new_crater = ImpactsEurope(
                        crater_name=row["crater_name"],
                        location=row["location"],
                        latitude=lat,
                        longitude=lon,
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