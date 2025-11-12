import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import text
from .database import engine
from .models import Base
from .routers import analyze, history, admin

app = FastAPI(title="URL Guardian", version="1.0.0")

# CORS (adjust in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(text("PRAGMA journal_mode=WAL")) if engine.url.get_backend_name() == "sqlite" else None

app.include_router(analyze.router)
app.include_router(history.router)
app.include_router(admin.router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
