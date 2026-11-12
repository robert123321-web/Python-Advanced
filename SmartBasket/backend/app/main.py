
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from . import models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SmartBasket API",
    description="Smart grocery shopping and meal planning platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "Welcome to SmartBasket!",
        "status": "Backend is running"
    }


@app.get("/api/health")
def health():
    return {
        "status": "healthy",
        "application": "SmartBasket"
    }
