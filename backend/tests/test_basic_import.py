"""Basic import tests to ensure CRUD endpoints are properly configured"""

def test_app_imports():
    """Test that main app imports successfully"""
    from app.main import app
    assert app is not None


def test_all_schemas_import():
    """Test that all schemas import successfully"""
    from app.schemas import (
        UserCreate, UserResponse,
        ClientCreate, ClientResponse,
        CraftsmanCreate, CraftsmanResponse,
        ProjectCreate, ProjectResponse,
        CampaignCreate, CampaignResponse,
        ItemCreate, ItemResponse,
        QuoteCreate, QuoteResponse,
        TaskCreate, TaskResponse,
    )
    # If we get here without ImportError, schemas are working
    assert True


def test_all_services_import():
    """Test that all services import successfully"""
    from app.services import (
        user_service,
        client_service,
        craftsman_service,
        project_service,
        campaign_service,
        item_service,
        quote_service,
        task_service,
    )
    # If we get here without ImportError, services are working
    assert True


def test_schema_validation():
    """Test basic schema validation works"""
    from app.schemas.user import UserCreate
    from app.schemas.project import ProjectCreate
    
    # Test user schema
    user_data = {
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "testpassword123"
    }
    user_create = UserCreate(**user_data)
    assert user_create.email == "test@example.com"
    assert user_create.full_name == "Test User"
    
    # Test project schema  
    project_data = {
        "name": "Test Project",
        "client_id": 1
    }
    project_create = ProjectCreate(**project_data)
    assert project_create.name == "Test Project"
    assert project_create.client_id == 1


def test_all_routers_import():
    """Test that all routers import successfully"""
    from app.routers.v1 import (
        users,
        clients,
        craftsmen,
        projects,
        campaigns,
        items,
        quotes,
        tasks,
    )
    # If we get here without ImportError, routers are working
    assert True