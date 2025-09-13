from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers.v1 import (
    health,
    users,
    clients,
    craftsmen,
    projects,
    campaigns,
    items,
    quotes,
    tasks,
)

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
app.include_router(users.router, prefix="/api/v1/users")
app.include_router(clients.router, prefix="/api/v1/clients")
app.include_router(craftsmen.router, prefix="/api/v1/craftsmen")
app.include_router(projects.router, prefix="/api/v1/projects")
app.include_router(campaigns.router, prefix="/api/v1/campaigns")
app.include_router(items.router, prefix="/api/v1/items")
app.include_router(quotes.router, prefix="/api/v1/quotes")
app.include_router(tasks.router, prefix="/api/v1/tasks")


@app.get("/")
async def root():
    return {
        "message": "StudioHub API - Design Studio Orchestration Platform",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
    }
