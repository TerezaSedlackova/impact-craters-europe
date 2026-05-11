from fastapi import FastAPI, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import sqlalchemy as db
from database import SessionLocal, engine, ImpactsEurope # Importujeme vše z database.py

app = FastAPI()

# Připojení složky se šablonami
templates = Jinja2Templates(directory="templates")

# Servírování statických souborů
app.mount("/static", StaticFiles(directory="static"), name="static")

#Obrázky
app.mount("/images", StaticFiles(directory="images"), name="images")



print("✅ Tabulka impacts_europe byla úspěšně vytvořena!")

def make_table():
    # ✅ Vytvoření tabulky (mělo by být provedeno pouze jednou)
    #Base.metadata.create_all(bind=engine)
    print("1")

#make_table()

@app.on_event("startup")
def on_startup():
    make_table()

# Dependency pro získání databázové session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

func_dict = {
   "next": next,
}

# ✅ Přidání endpointu pro kořenovou stránku "/"
@app.get("/")
async def read_root(request: Request):
    session = Session(engine)
    result = session.execute(db.text("SELECT * FROM impacts_europe"))
    craters = []
    for row in result:
        craters.append(zip(cols, row))
    return templates.TemplateResponse("index.html", {"request": request, "craters": craters, "next": next})
    #return {"message": "Vítejte na stránce impaktních kráterů!"}

# ✅ API endpoint pro získání všech kráterů
@app.get("/craters/")
def read_craters(session: Session = Depends(get_db)):
    #statement = db.select('impacts_europe')
    result = session.execute(db.text("SELECT * FROM impacts_europe"))
    craters = []
    for row in result:
        craters.append(zip(cols, row))
    return craters

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
