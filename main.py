print("MAIN APP LOADED")

from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from app.routes.ask import router as ask_router

app = FastAPI(title="DermaSenseAi")
app.include_router(ask_router, prefix="/api")

@app.get("/")
def health():
    return {"status": "ok"}