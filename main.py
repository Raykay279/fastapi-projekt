from fastapi import FastAPI
from db.database import database
from routers import buch_routes, benutzer_routes

app = FastAPI()

app.include_router(buch_routes.router)
app.include_router(benutzer_routes.router)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()