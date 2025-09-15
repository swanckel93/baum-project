"""Test configuration and fixtures"""

import pytest
import os
from fastapi.testclient import TestClient

from app.main import app
from app.core.database import get_db
from app.core.test_database import test_db_manager


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh PostgreSQL database for each test"""
    # Get the test node name for unique database naming
    test_name = os.environ.get('PYTEST_CURRENT_TEST', 'unknown_test')
    
    with test_db_manager.get_test_db_session(test_name) as session:
        yield session


@pytest.fixture(scope="function") 
def client(db_session):
    """Create a test client with database dependency override"""
    def get_test_db_override():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = get_test_db_override
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture(scope="session", autouse=True)
def verify_test_db_connection():
    """Verify PostgreSQL test database connection before running tests"""
    if not test_db_manager.verify_connection():
        pytest.exit(
            "Cannot connect to PostgreSQL test database. "
            "Please ensure Docker container is running:\n"
            "docker-compose -f docker-compose.test.yml up -d"
        )


@pytest.fixture
def sample_user_data():
    """Sample user data for testing"""
    return {
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "TestPassword123",
        "phone": "+1234567890",
        "is_active": True,
        "is_admin": False
    }


@pytest.fixture
def sample_client_data():
    """Sample client data for testing"""
    return {
        "name": "Test Client",
        "email": "client@example.com", 
        "phone": "+1234567890",
        "address": "123 Test Street, Test City",
        "notes": "Test client notes"
    }


@pytest.fixture
def sample_craftsman_data():
    """Sample craftsman data for testing"""
    return {
        "name": "Test Craftsman",
        "specialties": "Carpentry, Woodworking",
        "phone": "+1234567890",
        "email": "craftsman@example.com",
        "whatsapp": "+1234567890",
        "hourly_rate": "50.00",
        "notes": "Experienced craftsman",
        "is_active": True
    }


@pytest.fixture
def sample_project_data():
    """Sample project data for testing"""
    return {
        "name": "Test Project",
        "description": "A test project description",
        "status": "planning",
        "budget": "10000.00",
        "start_date": "2024-01-01",
        "end_date": "2024-12-31",
        "client_id": 1
    }


@pytest.fixture
def sample_campaign_data():
    """Sample campaign data for testing"""
    return {
        "name": "Test Campaign",
        "description": "A test campaign description", 
        "status": "active",
        "project_id": 1
    }


@pytest.fixture
def sample_item_data():
    """Sample item data for testing"""
    return {
        "name": "Test Item",
        "description": "A test item description",
        "quantity": 5,
        "unit": "unit",
        "estimated_cost": "100.00",
        "campaign_id": 1
    }


@pytest.fixture
def sample_quote_data():
    """Sample quote data for testing"""
    return {
        "price": "150.00",
        "currency": "EUR",
        "description": "Test quote description",
        "status": "pending",
        "margin_percentage": "20.00",
        "valid_until": "2025-12-31",
        "item_id": 1,
        "craftsman_id": 1
    }


@pytest.fixture
def sample_task_data():
    """Sample task data for testing"""
    return {
        "title": "Test Task",
        "description": "A test task description",
        "status": "todo",
        "priority": "medium",
        "due_date": "2024-06-01", 
        "project_id": 1,
        "assigned_user_id": 1
    }