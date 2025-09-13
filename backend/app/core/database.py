from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from .config import settings

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    # For PostgreSQL, we can use the default connection pool
    # StaticPool is used for SQLite in testing environments
    poolclass=StaticPool if "sqlite" in settings.DATABASE_URL else None,
    echo=settings.DEBUG,  # Log SQL queries in debug mode
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Dependency to get database session.
    This will be used with FastAPI's dependency injection.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()