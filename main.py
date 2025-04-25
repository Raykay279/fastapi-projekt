from fastapi import FastAPI
from fastapi import HTTPException
from typing import List
from pydantic import BaseModel

app = FastAPI()

# Datenmodell
class Buch(BaseModel):
    titel: str
    autor: str
    jahr: int
    isbn: str

# DB im Speicher
buecher_liste: List[Buch] = []

# Get-Route: alle Bücher anzeigen
@app.get("/buecher", response_model=List[Buch])
def get_buecher():
    return buecher_liste

# Post-Route: Ein Buch hinzufügen
@app.post("/buecher", response_model=Buch)
def add_buch(buch: Buch):
    buecher_liste.append(buch)
    return buch

# Suchabfrage einrichten
@app.get("/buecher/{isbn}", response_model=Buch)
def get_buch_by_id(isbn: str):
    for buch in buecher_liste:
        if buch.isbn == isbn:
            return buch
    # Falls kein Buch gefunden wird
    raise HTTPException(status_code=404, detail="Buch nicht gefunden")

# Deleteanfrage einrichten
@app.delete("/buecher/{isbn}", response_model=Buch)
def delete_buch(isbn: str):
    for index, buch in enumerate(buecher_liste):
        if buch.isbn == isbn:
            geloeschtes_buch = buecher_liste.pop(index)
            return geloeschtes_buch
    raise HTTPException(status_code=404, detail="Buch nicht gefunden")