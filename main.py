from fastapi import FastAPI
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