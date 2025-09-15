"""Test database management for per-test isolation"""

import time
import uuid
from typing import Generator
from contextlib import contextmanager

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError

from .config import settings
from ..models.base import Base


class TestDatabaseManager:
    """Manages test database lifecycle for isolated testing"""
    
    def __init__(self):
        self.template_db_url = settings.TEST_DATABASE_URL
        self.admin_db_url = f"postgresql://{settings.TEST_DB_USER}:{settings.TEST_DB_PASSWORD}@{settings.TEST_DB_HOST}:{settings.TEST_DB_PORT}/postgres"
        
    def _get_unique_db_name(self, test_name: str) -> str:
        """Generate unique database name for test"""
        timestamp = int(time.time() * 1000)
        unique_id = str(uuid.uuid4())[:8]
        # Clean test name for database naming
        clean_name = test_name.replace("::", "_").replace(".", "_").replace("[", "_").replace("]", "_")
        return f"test_{clean_name}_{timestamp}_{unique_id}"
    
    def _create_database(self, db_name: str) -> None:
        """Create a new test database"""
        try:
            # Connect to PostgreSQL server (not a specific database)
            conn = psycopg2.connect(
                host=settings.TEST_DB_HOST,
                port=settings.TEST_DB_PORT,
                user=settings.TEST_DB_USER,
                password=settings.TEST_DB_PASSWORD,
                database="postgres"
            )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            
            with conn.cursor() as cursor:
                # Create the test database
                cursor.execute(f'CREATE DATABASE "{db_name}"')
            
            conn.close()
            
        except psycopg2.Error as e:
            raise RuntimeError(f"Failed to create test database {db_name}: {e}")
    
    def _drop_database(self, db_name: str) -> None:
        """Drop a test database"""
        try:
            # Connect to PostgreSQL server
            conn = psycopg2.connect(
                host=settings.TEST_DB_HOST,
                port=settings.TEST_DB_PORT,
                user=settings.TEST_DB_USER,
                password=settings.TEST_DB_PASSWORD,
                database="postgres"
            )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            
            with conn.cursor() as cursor:
                # Terminate connections to the database before dropping
                cursor.execute(f"""
                    SELECT pg_terminate_backend(pg_stat_activity.pid)
                    FROM pg_stat_activity
                    WHERE pg_stat_activity.datname = '{db_name}'
                      AND pid <> pg_backend_pid()
                """)
                
                # Drop the test database
                cursor.execute(f'DROP DATABASE IF EXISTS "{db_name}"')
            
            conn.close()
            
        except psycopg2.Error as e:
            # Log the error but don't fail the test cleanup
            print(f"Warning: Failed to drop test database {db_name}: {e}")
    
    def _setup_schema(self, db_url: str) -> None:
        """Set up database schema using SQLAlchemy models"""
        try:
            engine = create_engine(db_url, echo=False)
            
            # Create all tables
            Base.metadata.create_all(bind=engine)
            
            engine.dispose()
            
        except SQLAlchemyError as e:
            raise RuntimeError(f"Failed to setup database schema: {e}")
    
    @contextmanager
    def get_test_db_session(self, test_name: str) -> Generator[Session, None, None]:
        """
        Context manager that provides an isolated database session for a test.
        
        Creates a new database, sets up schema, yields session, then cleans up.
        """
        db_name = self._get_unique_db_name(test_name)
        db_url = settings.get_test_db_url(db_name)
        
        try:
            # 1. Create database
            self._create_database(db_name)
            
            # 2. Setup schema
            self._setup_schema(db_url)
            
            # 3. Create session
            engine = create_engine(db_url, echo=False)
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            session = SessionLocal()
            
            try:
                yield session
            finally:
                session.close()
                engine.dispose()
                
        finally:
            # 4. Cleanup - always try to drop the database
            self._drop_database(db_name)
    
    def verify_connection(self) -> bool:
        """Verify that we can connect to the PostgreSQL test server"""
        try:
            conn = psycopg2.connect(
                host=settings.TEST_DB_HOST,
                port=settings.TEST_DB_PORT,
                user=settings.TEST_DB_USER,
                password=settings.TEST_DB_PASSWORD,
                database="postgres"
            )
            conn.close()
            return True
        except psycopg2.Error:
            return False


# Global instance
test_db_manager = TestDatabaseManager()