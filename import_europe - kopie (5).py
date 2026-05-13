import csv
import re
from sqlalchemy.orm import Session
from database import SessionLocal
from models import ImpactsEurope

def clean_coord(coord_str):
    """
    Převede souřadnice typu 'N 48° 45\'' na desetinné číslo (48.75).
    """
    if not coord_str or str(coord_str).lower() == "nan":
        return 0.0
    try:
        # Najde všechna čísla v řetězci (stupně a minuty)
        parts = re.findall(r'\d+', str(coord_str))
        if len(parts) >= 2:
            degrees = float(parts[0])
            minutes = float(parts[1])
            # Přepočet: stupně + (minuty / 60)
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
        # Ujistěte se, že soubor impacts_europe.csv je v hlavním adresáři projektu
        with open("impacts_europe.csv", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                lat = clean_coord(row["latitude"])
                lon = clean_coord(row["longitude"])
                
                # Kontrola, zda kráter již v databázi existuje podle jména
                existing = db.query(ImpactsEurope).filter(
                    ImpactsEurope.crater_name == row["crater_name"]
                ).first()

                # Získání hodnoty věku ze správného sloupce 'age_ma'
                age_val = float(row["age_ma"]) if row.get("age_ma") else 0.0

                if existing:
                    # AKTUALIZACE: Přepsání starých dat novými (včetně opravy souřadnic)
                    existing.latitude = lat
                    existing.longitude = lon
                    existing.location = row["location"]
                    existing.diameter_km = float(row["diameter_km"]) if row["diameter_km"] else 0.0
                    existing.age_million_years = age_val
                else:
                    # NOVÝ ZÁZNAM: Pokud v databázi ještě není
                    new_crater = ImpactsEurope(
                        crater_name=row["crater_name"],
                        location=row["location"],
                        latitude=lat,
                        longitude=lon,
                        diameter_km=float(row["diameter_km"]) if row["diameter_km"] else 0.0,
                        age_million_years=age_val,
                        exposed=row["exposed"],
                        drilled=row["drilled"],
                        target_rock=row["target_rock"],
                        bolide_type=row["bolide_type"]
                    )
                    db.add(new_crater)
                    
        db.commit()
        print("✅ Evropské krátery byly úspěšně importovány/aktualizovány!")
    except Exception as e:
        db.rollback()
        print(f"❌ Chyba při importu: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    import_european_craters()