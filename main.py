from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def startseite():
    return {"Nachricht": "Herzlich Willkommen auf meinem FastAPI-Server!"}