from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import os

from database import engine, SessionLocal, Base, ImpactsEurope
from import_europe import import_european_craters

# Vytvoření databázových tabulek (pokud neexistují)
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Připojení statických souborů a šablon
app.mount("/static", StaticFiles(directory="static"), name="static")
# Pokud máte obrázky v samostatné složce 'images'
if os.path.exists("images"):
    app.mount("/images", StaticFiles(directory="images"), name="images")

templates = Jinja2Templates(directory="templates")

# Dependency pro získání DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup_event():
    # Automatický import dat při startu aplikace
    print("Spouštím automatický import dat...")
    import_european_craters()

@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request, db: Session = Depends(get_db)):
    # Načtení všech kráterů z databáze
    craters = db.query(ImpactsEurope).all()
    
    # Předání seznamu objektů do šablony index.html
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "craters": craters}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)