from datetime import datetime

import redis
from fastapi import APIRouter, HTTPException

from app.core.config import settings

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check():
    """
    Health check endpoint that verifies all critical services are running.
    Returns detailed status of database, Redis, and application.
    """
    status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "services": {
            "database": "unknown",
            "redis": "unknown",
            "application": "healthy",
        },
    }

    # Check Redis connection
    try:
        redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
        redis_client.ping()
        status["services"]["redis"] = "healthy"
        redis_client.close()
    except Exception as e:
        status["services"]["redis"] = f"unhealthy: {str(e)}"
        status["status"] = "degraded"

    # For now, assume database is healthy (we'll implement proper check when DB is set up)
    status["services"]["database"] = "not_configured"

    if status["status"] != "healthy":
        raise HTTPException(status_code=503, detail=status)

    return status


@router.get("/health/simple")
async def simple_health_check():
    """Simple health check that just returns OK if the API is running."""
    return {"status": "ok", "message": "StudioHub API is running"}
