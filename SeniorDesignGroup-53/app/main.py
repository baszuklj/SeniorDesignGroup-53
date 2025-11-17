import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import text
from pathlib import Path

from .database import engine
from .models import Base
from .routers import analyze, history, admin

app = FastAPI(title="URL Guardian", version="1.0.0")

# CORS...
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR = Path(__file__).resolve().parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/", include_in_schema=False)
def home():
    return FileResponse(STATIC_DIR / "index.html")

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(analyze.router)
app.include_router(history.router)
app.include_router(admin.router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
