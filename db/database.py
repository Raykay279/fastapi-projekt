from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from databases import Database

# Verbindung zur SQLite-DB herstellen
DATABASE_URL = "sqlite:///./bibliothek.db"

database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Tabelle für die Bücher definieren

buecher = Table(
    "buecher",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("titel", String),
    Column("autor", String),
    Column("jahr", Integer),
    Column("isbn", String),
)

# Tabelle für die User definieren

benutzer = Table(
    "benutzer",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, unique=True, index=True),
    Column("name", String),
    Column("passwort", String),
    )

metadata.create_all(engine)