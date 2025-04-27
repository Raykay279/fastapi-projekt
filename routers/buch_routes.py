from fastapi import APIRouter, HTTPException
from typing import List
from models.buch import Buch, BuchUpdate
from db.database import database, buecher

router = APIRouter()

@router.get("/buecher", response_model=List[Buch])
async def get_buecher():
    query = buecher.select()
    return await database.fetch_all(query)

@router.post("/buecher", response_model=Buch)
async def add_buch(buch: Buch):
    query = buecher.insert().values(
        titel=buch.titel,
        autor=buch.autor,
        jahr=buch.jahr,
        isbn=buch.isbn,
    )
    await database.execute(query)
    return buch

@router.get("/buecher/{isbn}", response_model=Buch)
async def get_buch_by_id(isbn: str):
    query = buecher.select().where(buecher.c.isbn == isbn)
    buch = await database.fetch_one(query)
    if buch is None:
        raise HTTPException(status_code=404, detail="Buch nicht gefunden")
    return buch

@router.delete("/buecher/{isbn}", response_model=Buch)
async def delete_buch(isbn: str):
    query = buecher.select().where(buecher.c.isbn == isbn)
    buch = await database.fetch_one(query)
    if buch is None:
        raise HTTPException(status_code=404, detail="Buch nicht gefunden")

    delete_query = buecher.delete().where(buecher.c.isbn == isbn)
    await database.execute(delete_query)
    return buch

@router.put("/buecher/{isbn}", response_model=Buch)
async def update_buch(isbn: str, aktualisiertes_buch: Buch):
    query = buecher.select().where(buecher.c.isbn == isbn)
    buch = await database.fetch_one(query)
    if buch is None:
        raise HTTPException(status_code=404, detail="Buch nicht gefunden")

    update_query = (
        buecher.update()
        .where(buecher.c.isbn == isbn)
        .values(
            titel=aktualisiertes_buch.titel,
            autor=aktualisiertes_buch.autor,
            jahr=aktualisiertes_buch.jahr,
            isbn=aktualisiertes_buch.isbn,
        )
    )
    await database.execute(update_query)
    return aktualisiertes_buch

@router.patch("/buecher/{isbn}", response_model=Buch)
async def patch_buch(isbn: str, buchpatch: BuchUpdate):
    query = buecher.select().where(buecher.c.isbn == isbn)
    buch = await database.fetch_one(query)
    if buch is None:
        raise HTTPException(status_code=404, detail="Buch nicht gefunden")

    buchdaten = dict(buch)
    buchpatchdaten = buchpatch.dict(exclude_unset=True)
    buchdaten.update(buchpatchdaten)

    update_query = (
        buecher.update()
        .where(buecher.c.isbn == isbn)
        .values(
            titel=buchdaten["titel"],
            autor=buchdaten["autor"],
            jahr=buchdaten["jahr"],
            isbn=buchdaten["isbn"],
        )
    )
    await database.execute(update_query)
    return buchdaten