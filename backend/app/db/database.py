from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.session import engine, Base

@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield
