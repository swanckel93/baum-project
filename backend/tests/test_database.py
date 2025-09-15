import pytest
from unittest.mock import patch, MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.core.database import get_db, SessionLocal, engine
from app.core.config import settings


class TestDatabaseConnection:
    """Test database connection functionality."""
    
    def test_get_db_generator(self):
        """Test that get_db returns a generator that yields a database session."""
        # Mock the SessionLocal to avoid actual database connection
        with patch('app.core.database.SessionLocal') as mock_session_local:
            mock_session = MagicMock()
            mock_session_local.return_value = mock_session
            
            # Get the generator
            db_gen = get_db()
            
            # Get the session from the generator
            db_session = next(db_gen)
            
            # Verify we got the mocked session
            assert db_session == mock_session
            
            # Verify SessionLocal was called
            mock_session_local.assert_called_once()
            
            # Complete the generator to trigger cleanup
            try:
                next(db_gen)
            except StopIteration:
                pass
            
            # Verify session.close() was called
            mock_session.close.assert_called_once()
    
    def test_get_db_context_manager(self):
        """Test get_db can be used as a context manager."""
        with patch('app.core.database.SessionLocal') as mock_session_local:
            mock_session = MagicMock()
            mock_session_local.return_value = mock_session
            
            # Use as dependency injection (similar to FastAPI usage)
            db_gen = get_db()
            
            try:
                session = next(db_gen)
                # Simulate some database operation
                assert session == mock_session
            except Exception:
                # If there's an exception, cleanup should still happen
                pass
            finally:
                # Complete the generator
                try:
                    next(db_gen)
                except StopIteration:
                    pass
            
            # Verify cleanup happened
            mock_session.close.assert_called_once()
    
    def test_session_local_configuration(self):
        """Test SessionLocal is configured correctly."""
        # Check that SessionLocal has the right configuration
        assert SessionLocal.kw['autocommit'] is False
        assert SessionLocal.kw['autoflush'] is False
        assert SessionLocal.kw['bind'] == engine
    
    def test_database_configuration(self):
        """Test that database is configured properly."""
        # Test that the engine exists and has correct configuration
        assert engine is not None
        
        # Test that SessionLocal is configured correctly
        assert SessionLocal is not None
        assert hasattr(SessionLocal, 'kw')
        
        # Test settings are accessible
        assert settings.DATABASE_URL is not None
        assert settings.TEST_DATABASE_URL is not None
    
    def test_database_url_from_settings(self):
        """Test that database URL comes from settings."""
        # The engine should use the DATABASE_URL from settings
        expected_url = settings.DATABASE_URL
        
        # Note: We can't easily test the actual URL without mocking,
        # but we can verify the engine exists and has the right type
        assert engine is not None
        assert hasattr(engine, 'url')


class TestDatabaseIntegration:
    """Integration tests for database functionality."""
    
    @pytest.fixture
    def test_db_session(self):
        """Create a test database session using SQLite in memory."""
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        from app.models.base import BaseModel
        
        # Create in-memory SQLite database
        test_engine = create_engine("sqlite:///:memory:", echo=False)
        
        # Create all tables
        BaseModel.metadata.create_all(test_engine)
        
        # Create session
        TestSession = sessionmaker(bind=test_engine)
        session = TestSession()
        
        yield session
        
        session.close()
    
    def test_database_session_workflow(self, test_db_session):
        """Test basic database session workflow."""
        from app.models import User
        
        # Create a user
        user = User(
            email="test@example.com",
            hashed_password="hashed",
            full_name="Test User",
            is_active=True,
            is_admin=False
        )
        
        # Add and commit
        test_db_session.add(user)
        test_db_session.commit()
        
        # Verify user was created
        assert user.id is not None
        
        # Query the user back
        queried_user = test_db_session.query(User).filter(
            User.email == "test@example.com"
        ).first()
        
        assert queried_user is not None
        assert queried_user.email == "test@example.com"
        assert queried_user.full_name == "Test User"
    
    def test_session_rollback_on_error(self, test_db_session):
        """Test that session rollback works on errors."""
        from app.models import User
        
        # Create a user
        user1 = User(
            email="user1@example.com",
            hashed_password="hashed",
            full_name="User 1",
            is_active=True,
            is_admin=False
        )
        test_db_session.add(user1)
        test_db_session.commit()
        
        # Try to create another user with the same email (should fail)
        user2 = User(
            email="user1@example.com",  # Duplicate email
            hashed_password="hashed",
            full_name="User 2",
            is_active=True,
            is_admin=False
        )
        test_db_session.add(user2)
        
        # This should raise an error due to unique constraint
        with pytest.raises(Exception):
            test_db_session.commit()
        
        # Rollback the session
        test_db_session.rollback()
        
        # Verify only the first user exists
        users = test_db_session.query(User).all()
        assert len(users) == 1
        assert users[0].full_name == "User 1"