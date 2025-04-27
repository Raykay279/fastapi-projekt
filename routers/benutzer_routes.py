from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from models.benutzer import BenutzerIn
from auth.security import hash_passwort, pwd_context, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTEN
from db.database import database, benutzer
from datetime import timedelta

router = APIRouter()

@router.post("/registrieren")
async def registrieren(benutzer_in: BenutzerIn):
    hashed_passwort = hash_passwort(benutzer_in.passwort)

    query = benutzer.insert().values(
        email=benutzer_in.email,
        name=benutzer_in.name,
        passwort=hashed_passwort
    )

    await database.execute(query)
    return {"message": "Benutzer erfolgreich registriert"}

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    query = benutzer.select().where(benutzer.c.email == form_data.username)
    user = await database.fetch_one(query)

    if not user:
        raise HTTPException(status_code=400, detail="Ungültige Zugangsdaten")

    if not pwd_context.verify(form_data.password, user["passwort"]):
        raise HTTPException(status_code=400, detail="Ungültiges Passwort")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTEN)
    access_token = create_access_token(
        data={"sub": user["email"]},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}