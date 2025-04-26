from fastapi import FastAPI
from fastapi import HTTPException
from typing import List
from pydantic import BaseModel

app = FastAPI()

# Datenmodell Film
class Film(BaseModel):
    titel: str
    genre: str
    jahr: int
    favorit: bool

# DB im Speicher
filmliste: List[Film] = []

# Abfrage der Filmliste
@app.get("/filme", response_model=List[Film])
def abruf():
    return filmliste

# Einreichen neuer Film
@app.post("/filme", response_model=Film)
def add(film: Film):
    filmliste.append(film)
    return film

# Suchabfrage
@app.get("/filme/{titel}", response_model=Film)
def search(titel: str):
    for film in filmliste:
        if titel.lower() == film.titel.lower():
            return film
    raise HTTPException(status_code=404, detail="Film nicht gefunden")

# Löschanfrage
@app.delete("/filme/{titel}", response_model=Film)
def remove(titel: str):
    for index, film in enumerate(filmliste):
        if titel.lower() == film.titel.lower():
            geloeschter_film = filmliste.pop(index)
            return geloeschter_film
    raise HTTPException(status_code=404, detail="Gibts nicht")  