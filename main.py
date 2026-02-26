print("MAIN APP LOADED")

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from app.routes.ask import router as ask_router
from app.services.memory_service import init_db

app = FastAPI(
    title="DermaSense AI",
    version="1.0.0"
)

@app.on_event("startup")
def startup_event():
    print("Initializing SQLite database...")
    init_db()
    print("Database ready.")

app.include_router(ask_router, prefix="/api")





@app.get("/")
def health():
    return {"status": "ok"}