import csv
import re
from sqlalchemy.orm import Session
from database import SessionLocal
from models import ImpactsEurope

def parse_num(val):
    if not val or str(val).strip() in ["-", "nan", ""]: return 0.0
    # Extrahuje první číslo (i s tečkou) z textu
    nums = re.findall(r"[-+]?\d*\.\d+|\d+", str(val).replace(",", "."))
    return float(nums[0]) if nums else 0.0

def clean_coord(s):
    if not s or "nan" in str(s).lower(): return 0.0
    p = re.findall(r'\d+', str(s))
    if len(p) >= 2: return round(float(p[0]) + (float(p[1]) / 60.0), 4)
    return float(p[0]) if p else 0.0

def import_european_craters():
    db = SessionLocal()
    try:
        with open("impacts_europe.csv", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader:
                lat, lon = clean_coord(r["latitude"]), clean_coord(r["longitude"])
                dia, age = parse_num(r.get("diameter_km")), parse_num(r.get("age_ma"))
                
                item = db.query(ImpactsEurope).filter_by(crater_name=r["crater_name"]).first()
                if not item:
                    item = ImpactsEurope(crater_name=r["crater_name"])
                    db.add(item)
                
                item.location, item.latitude, item.longitude = r["location"], lat, lon
                item.diameter_km, item.age_million_years = dia, age
                item.exposed, item.drilled = r["exposed"], r["drilled"]
                item.target_rock, item.bolide_type = r["target_rock"], r["bolide_type"]
        db.commit()
        print("✅ Import/Aktualizace dokončena.")
    except Exception as e:
        print(f"❌ Chyba: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    import_european_craters()