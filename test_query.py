from sqlalchemy import text, create_engine

DATABASE_URL = "sqlite:///impacts_europe.db"
engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM impacts_europe LIMIT 5"))
    rows = result.fetchall()

    if rows:
        print("✅ Načteno několik záznamů přímo z tabulky:")
        for row in rows:
            print(row)
    else:
        print("🛑 Tabulka impacts_europe je prázdná.")
