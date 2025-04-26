from database import database, buecher
from fastapi import FastAPI
from fastapi import HTTPException
from typing import List
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

# DB Verbindung
@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Datenmodell Buch
class Buch(BaseModel):
    titel: str
    autor: str
    jahr: int
    isbn: str

# Dantenmodell Buch update
class BuchUpdate(BaseModel):
    titel: Optional[str] = None
    autor: Optional[str] = None
    jahr: Optional[str] = None
    isbn: Optional[str] = None


# Get-Route: alle Bücher anzeigen
@app.get("/buecher", response_model=List[Buch])
async def get_buecher():
    query = buecher.select()
    return await database.fetch_all(query)

# Post-Route: Ein Buch hinzufügen
@app.post("/buecher", response_model=Buch)
async def add_buch(buch: Buch):
    query = buecher.insert().values(
    titel=buch.titel,
    autor=buch.autor,
    jahr=buch.jahr,
    isbn=buch.isbn,
    )
    await database.execute(query)
    return buch

# Suchabfrage einrichten
@app.get("/buecher/{isbn}", response_model=Buch)
async def get_buch_by_id(isbn: str):
    query = buecher.select().where(buecher.c.isbn == isbn)
    buch = await database.fetch_one(query)
    if buch is None:
    # Falls kein Buch gefunden wird
        raise HTTPException(status_code=404, detail="Buch nicht gefunden")
    return buch

# Deleteanfrage einrichten
@app.delete("/buecher/{isbn}", response_model=Buch)
async def delete_buch(isbn: str):
    # Zuerst prüfen ob das Buch existiert
    query = buecher.select().where(buecher.c.isbn == isbn)
    buch = await database.fetch.one(query)
    if buch is None:
        raise HTTPException(status_code=404, detail="Buch nicht gefunden")
    
    # Jetzt wirklich löschen
    delete_query = buecher.delete().where(buecher.c.isbn == isbn)
    await database.execute(delete_query)

    return buch

# Buchersetzung
@app.put("/buecher/{isbn}", response_model=Buch)
async def update_buch(isbn: str, aktualisiertes_buch: Buch):
    query = buecher.select().where(buecher.c.isbn == isbn)
    buch = await database.fetch_one(query)
    if buch is None:
        raise HTTPException(status_code=404, "Buch nicht gefunden")
    update_query = (
        buecher.update()
        .where(buecher.c.isbn == isbn)
        .values(
            titel = aktualisiertes_buch.titel,
            autor = aktualisiertes_buch.autor,
            jahr = aktualisiertes_buch.jahr,
            isbn = aktualisiertes_buch.isbn,
        )
    )
    await database.execute(update_query)
    return aktualisiertes_buch
   

# Teilupdate eines Buches
@app.patch("/buecher/{isbn}", response_model=Buch)
def patch_buch(isbn: str, buchupdate: BuchUpdate):
    for index, buch in enumerate(buecher_liste):
        if buch.isbn == isbn:
            buchdaten = buch.dict()
            buchupdatedaten = buchupdate.dict(exclude_unset=True)
            buchdaten.update(buchupdatedaten)
            buecher_liste[index] = Buch(**buchdaten)
            return buecher_liste[index]
    raise HTTPException(status_code=404, detail="Buch nicht gefunden")