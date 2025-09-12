from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers.v1 import health

app = FastAPI(
    title="StudioHub API",
    description="Design Studio Orchestration Platform for Estudio Baum Arquitectos",
    version="1.0.0",
    docs_url="/docs" if settings.ENVIRONMENT == "development" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT == "development" else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "message": "StudioHub API - Design Studio Orchestration Platform",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT
    }