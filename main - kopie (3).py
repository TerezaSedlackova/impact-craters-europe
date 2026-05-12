from fastapi import FastAPI, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import sqlalchemy as db
from database import SessionLocal, engine, ImpactsEurope
import uvicorn

app = FastAPI()

# Konfigurace šablon a statických souborů
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/images", StaticFiles(directory="images"), name="images")

# Definice sloupců pro mapování výsledků textových dotazů
cols = (
    'id', 'crater_name', 'location', 'latitude', 'longitude', 
    'diameter_km', 'age_million_years', 'exposed', 'drilled', 
    'target_rock', 'bolide_type'
)

# Dependency pro databázovou session
def get_db():
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()

@app.get("/")
async def read_root(request: Request, db_session: Session = Depends(get_db)):
    # Použití ORM modelu ImpactsEurope namísto raw SQL pro vyšší bezpečnost
    result = db_session.query(ImpactsEurope).all()
    return templates.TemplateResponse("index.html", {"request": request, "craters": result})

@app.get("/craters/")
def read_craters(db_session: Session = Depends(get_db)):
    craters = db_session.query(ImpactsEurope).all()
    return craters

if __name__ == "__main__":
    # V produkci reload=False a port lze měnit dle potřeby
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)