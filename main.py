from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import os

from database import engine, SessionLocal, Base
from models import ImpactsEurope
from import_europe import import_european_craters

# Vytvoření databázových tabulek
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Připojení statických souborů
app.mount("/static", StaticFiles(directory="static"), name="static")

# Mountování složky s obrázky, pokud existuje
if os.path.exists("images"):
    app.mount("/images", StaticFiles(directory="images"), name="images")

templates = Jinja2Templates(directory="templates")

# Mapovací slovník zdrojů obrázků
IMAGE_SOURCES = {
    "boltysh": {"name": "Wikipedia", "url": "https://cs.wikipedia.org/wiki/Bolty%C5%A1"},
    "dellen": {"name": "Wikipedia", "url": "https://en.wikipedia.org/wiki/Dellen"},
    "dobele": {"name": "Vecteezy", "url": "https://www.vecteezy.com/photo/2898813-dobele-castle-ruins-in-dobele-latvia"},
    "gardnos": {"name": "Wikipedia", "url": "https://cs.wikipedia.org/wiki/Soubor:Gardnos-overview.jpg"},
    "granby": {"name": "Depositphotos", "url": "https://depositphotos.com/cz/photo/meteor-impact-crater-coconino-county-arizona-usa-flagstaff-367751036.html"},
    "hummeln": {"name": "Lake Scientist", "url": "https://www.lakescientist.com/space-rock-created-swedens-hummeln-lake/"},
    "ilumetsä": {"name": "Wikipedia", "url": "https://cs.wikipedia.org/wiki/Ilumetsk%C3%A9_kr%C3%A1tery"},
    "ilyinets": {"name": "UAIN Press", "url": "https://uain.press/articles/zoryani-rani-ukrayini-1073077/attachment/illinetskij-krater"},
    "iso-naakkima": {"name": "Wikipedia", "url": "https://fi.wikipedia.org/wiki/Iso-Naakkima"},
    "kaalijärv": {"name": "Liceo Desio", "url": "https://spark.liceodesio.edu.it/mod/wiki/prettyview.php?pageid=109"},
    "kärdla": {"name": "Daytrip", "url": "https://daytrip.com/en/day-trips/from-tallinn/lahemaa-national-park"},
    "karikkoselkä": {"name": "Springer", "url": "https://link.springer.com/chapter/10.1007/978-3-030-05451-9_94"},
    "lappajärvi": {"name": "Lappajärvi FI", "url": "https://lappajarvi.fi/kraatterijarvi-geopark-on-nyt-virallisesti-suomen-viides-unesco-global-geopark/"},
    "lockne": {"name": "Technologijos", "url": "https://m.technologijos.lt/cat/1/article/S-43683"},
    "lumparn": {"name": "Lomner", "url": "https://lomner.se/another-evening-at-lumparn/"},
    "målingen": {"name": "Technologijos", "url": "https://m.technologijos.lt/cat/1/article/S-43683"},
    "mien": {"name": "PASSC", "url": "http://www.passc.net/EarthImpactDatabase/New%20website_05-2018/Mien.html"},
    "mizarai": {"name": "Atrask Dzūkija", "url": "https://www.atraskdzukija.lt/en/sightseeing-places/mi/"},
    "mjølnir": {"name": "NASA APOD", "url": "https://apod.nasa.gov/apod/ap990610.html"},
    "morasko": {"name": "Facebook", "url": "https://www.facebook.com/geol.uam/posts/geoparki-w-polsce-a-potencja%C5%82-przyrodniczo-kulturowy-poznania-i-okolicz-przyjemn/2905925192965629/"},
    "neugrund": {"name": "ResearchGate", "url": "https://www.researchgate.net/figure/Location-of-the-Neugrund-and-other-partially-or-completely-marine-impact-structures_fig1_228805905"},
    "obolon'": {"name": "Universe Magazine", "url": "https://universemagazine.com/en/catastrophe-remnants-where-meteorite-craters-are-preserved-in-ukraine/"},
    "paasselkä": {"name": "ResearchGate", "url": "https://www.researchgate.net/figure/Landsat-7-satellite-image-scene-of-the-Paasselkae-impact-structure-and-position-in-SE_fig2_230288405"},
    "ries": {"name": "Lieslotte", "url": "https://termine.lieslotte.de/event/geopark-fuehrung-sagenhafter-wennenberg/"},
    "ritland": {"name": "DNT", "url": "https://www.dnt.no/dnt-der-du-er/stavanger/hjelmeland-turlag/vare-hytter/"},
    "rochechouart": {"name": "Wikipedia", "url": "https://zh.wikipedia.org/wiki/File:Rochechouart-Schloss_17.JPG"},
    "rotmistrovka": {"name": "Wikipedia", "url": "https://en.wikipedia.org/wiki/Rotmistrivka_crater"},
    "siljan": {"name": "ESA", "url": "https://www.esa.int/ESA_Multimedia/Images/2016/02/Colours_of_Sweden"},
    "steinheim": {"name": "Schreiber Weinert", "url": "https://www.schreiber-weinert.de/en/nach-meteoriteneinschlag-im-steinheimer-becken-schreiber-weinert-beliefert-eine-vielzahl-von-unternehmen/"},
    "vepriai": {"name": "Wikipedia", "url": "https://cs.wikipedia.org/wiki/Soubor:Mokas_ir_mokiukas_2014.jpg"},
    "kara": {"name": "Rusline", "url": "https://www.rusline.aero/blog/6-must-visit-mest-karelii/"},
    "karla": {"name": "Ege Telgraf", "url": "https://www.egetelgraf.com/nemrut-krater-golu-kis-manzarasiyla-buyuluyor"},
    "kamensk": {"name": "Iskatel", "url": "https://iskatel.com/places/dlinnyy-kanon"}
}

# Překladové slovníky pro backend
LOCATION_TRANSLATIONS = {
    "ukraine": "Ukrajina",
    "sweden": "Švédsko",
    "finland": "Finsko",
    "estonia": "Estonsko",
    "norway": "Norsko",
    "germany": "Německo",
    "france": "Francie",
    "russia": "Rusko",
    "latvia": "Lotyšsko",
    "lithuania": "Litva",
    "poland": "Polsko",
    "belarus": "Bělorusko"
}

BOLIDE_TRANSLATIONS = {
    "stone": "Kamenné těleso",
    "stony": "Kamenné těleso",
    "octahedrite fragments": "Fragmenty oktaedritu",
    "achondrite": "Achondrit",
    "stony-iron": "Kamenoželezné těleso",
    "iron": "Železné těleso",
    "chondrite": "Chondrit"
}

# Dependency pro získání DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup_event():
    print("Inicializace databáze a kontrola souřadnic...")
    import_european_craters()

@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request, db: Session = Depends(get_db)):
    craters = db.query(ImpactsEurope).all()
    
    for crater in craters:
        # Mapování zdrojů obrázků
        key = crater.crater_name.lower().strip() if crater.crater_name else ""
        if key in IMAGE_SOURCES:
            crater.image_source = IMAGE_SOURCES[key]["name"]
            crater.image_source_url = IMAGE_SOURCES[key]["url"]
        else:
            crater.image_source = None
            crater.image_source_url = None

        # Překlad lokality (ošetření otazníků)
        if crater.location:
            loc_raw = crater.location.lower().strip()
            has_question = "?" in loc_raw
            loc_key = loc_raw.replace("?", "").strip()
            
            if loc_key in LOCATION_TRANSLATIONS:
                crater.location = LOCATION_TRANSLATIONS[loc_key] + ("?" if has_question else "")

        # Překlad typu dopadového tělesa (ošetření otazníků)
        if crater.bolide_type:
            bol_raw = crater.bolide_type.lower().strip()
            has_question = "?" in bol_raw
            bol_key = bol_raw.replace("?", "").strip()
            
            if bol_key in BOLIDE_TRANSLATIONS:
                crater.bolide_type = BOLIDE_TRANSLATIONS[bol_key] + ("?" if has_question else "")
            
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "craters": craters}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)