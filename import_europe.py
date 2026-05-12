import csv
import re
from sqlalchemy.orm import Session
from database import SessionLocal
from models import ImpactsEurope

def clean_coord(coord_str):
    if not coord_str or str(coord_str).lower() == "nan":
        return 0.0
    try:
        parts = re.findall(r'\d+', str(coord_str))
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

def parse_numeric_value(value_str):
    """
    Extrahuje číslo z textu jako '65.17 ± 0.64', '1.2-4' nebo '~ 1.2'.
    V případě rozsahu (1.2-4) vypočítá průměr.
    """
    if not value_str or str(value_str).strip() in ["-", "nan", ""]:
        return 0.0
    
    # Odstranění vlnovek a mezer
    clean_val = str(value_str).replace("~", "").strip()
    
    # Hledání všech čísel (včetně desetinných teček)
    numbers = re.findall(r"[-+]?\d*\.\d+|\d+", clean_val.replace(",", "."))
    
    if not numbers:
        return 0.0
    
    if len(numbers) >= 2 and "-" in clean_val:
        # Pokud je to rozsah (např. 1.2-4), spočítáme průměr
        return (float(numbers[0]) + float(numbers[1])) / 2
    
    # Jinak vezmeme první nalezené číslo (ignorujeme odchylku ±)
    return float(numbers[0])

def import_european_craters():
    db: Session = SessionLocal()
    try:
        with open("impacts_europe.csv", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                lat = clean_coord(row["latitude"])
                lon = clean_coord(row["longitude"])
                
                # Použití nové funkce pro průměr a věk
                diameter = parse_numeric_value(row.get("diameter_km"))
                age = parse_numeric_value(row.get("age_ma"))

                existing = db.query(ImpactsEurope).filter(
                    ImpactsEurope.crater_name == row["crater_name"]
                ).first()

                if existing:
                    existing.latitude = lat
                    existing.longitude = lon
                    existing.location = row["location"]
                    existing.diameter_km = diameter
                    existing.age_million_years = age
                else:
                    new_crater = ImpactsEurope(
                        crater_name=row["crater_name"],
                        location=row["location"],
                        latitude=lat,
                        longitude=lon,
                        diameter_km=diameter,
                        age_million_years=age,
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