from pydantic import BaseModel

class BenutzerIn(BaseModel):
    email: str
    name: str
    passwort: str