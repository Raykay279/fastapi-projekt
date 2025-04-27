from pydantic import BaseModel
from typing import Optional

class Buch(BaseModel):
    titel: str
    autor: str
    jahr: str
    isbn: str

class BuchUpdate(BaseModel):
    titel: Optional[str] = None
    autor: Optional[str] = None
    jahr: Optional[str] = None
    isbn: Optional[str] = None