sqlite3
.mode ascii
.separator "," "\n"
DROP TABLE impacts_europe;
--CREATE TABLE impacts_europe ( crater_name VARCHAR,    location VARCHAR,    latitude VARCHAR,    longitude VARCHAR,    diameter_km VARCHAR,    age_million_years VARCHAR,    exposed VARCHAR,    drilled VARCHAR,    target_rock VARCHAR,    bolide_type VARCHAR);
--Tabulka se vytvoří automaticky
.import impacts_europe.csv impacts_europe 
--Ukáže tabulku
SELECT * FROM impacts_europe; 
.save impacts_europe.db
uvicorn main:app --reload