from datetime import date
from decimal import Decimal

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.models import (
    Campaign,
    CampaignStatus,
    Client,
    Craftsman,
    Currency,
    Item,
    Project,
    ProjectStatus,
    Quote,
    QuoteStatus,
    Task,
    TaskPriority,
    TaskStatus,
    Unit,
    User,
)
from app.models.base import BaseModel


@pytest.fixture
def db_session():
    """Create an in-memory SQLite database for testing."""
    engine = create_engine("sqlite:///:memory:", poolclass=StaticPool, echo=False)

    # Create all tables
    BaseModel.metadata.create_all(engine)

    # Create session
    test_session = sessionmaker(bind=engine)
    session = test_session()

    yield session

    session.close()


@pytest.fixture
def sample_user(db_session):
    """Create a sample user for testing."""
    user = User(
        email="test@example.com",
        hashed_password="hashed_password_here",
        full_name="Test User",
        phone="+34123456789",
        is_active=True,
        is_admin=False,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def sample_client(db_session):
    """Create a sample client for testing."""
    client = Client(
        name="Test Client",
        email="client@example.com",
        phone="+34987654321",
        whatsapp="+34987654321",
        address="123 Test Street, Barcelona",
        company="Test Company SL",
    )
    db_session.add(client)
    db_session.commit()
    db_session.refresh(client)
    return client


@pytest.fixture
def sample_craftsman(db_session):
    """Create a sample craftsman for testing."""
    craftsman = Craftsman(
        name="Test Craftsman",
        email="craftsman@example.com",
        phone="+34555666777",
        whatsapp="+34555666777",
        specialties="carpentry,plumbing",
        hourly_rate=Decimal("25.50"),
        is_active=True,
    )
    db_session.add(craftsman)
    db_session.commit()
    db_session.refresh(craftsman)
    return craftsman


class TestUserModel:
    """Test User model functionality."""

    def test_create_user(self, db_session):
        """Test creating a user."""
        user = User(
            email="newuser@example.com",
            hashed_password="hashed_password",
            full_name="New User",
            is_active=True,
            is_admin=False,
        )
        db_session.add(user)
        db_session.commit()

        assert user.id is not None
        assert user.email == "newuser@example.com"
        assert user.full_name == "New User"
        assert user.is_active is True
        assert user.is_admin is False
        assert user.created_at is not None

    def test_user_repr(self, sample_user):
        """Test user string representation."""
        expected = f"<User(id={sample_user.id}, email='test@example.com', full_name='Test User')>"
        assert repr(sample_user) == expected


class TestClientModel:
    """Test Client model functionality."""

    def test_create_client(self, db_session):
        """Test creating a client."""
        client = Client(
            name="New Client", email="newclient@example.com", company="New Company"
        )
        db_session.add(client)
        db_session.commit()

        assert client.id is not None
        assert client.name == "New Client"
        assert client.email == "newclient@example.com"
        assert client.company == "New Company"
        assert client.created_at is not None

    def test_client_repr(self, sample_client):
        """Test client string representation."""
        expected = f"<Client(id={sample_client.id}, name='Test Client', email='client@example.com')>"
        assert repr(sample_client) == expected


class TestCraftsmanModel:
    """Test Craftsman model functionality."""

    def test_create_craftsman(self, db_session):
        """Test creating a craftsman."""
        craftsman = Craftsman(
            name="New Craftsman", specialties="electrical", is_active=True
        )
        db_session.add(craftsman)
        db_session.commit()

        assert craftsman.id is not None
        assert craftsman.name == "New Craftsman"
        assert craftsman.specialties == "electrical"
        assert craftsman.is_active is True
        assert craftsman.created_at is not None

    def test_craftsman_repr(self, sample_craftsman):
        """Test craftsman string representation."""
        expected = f"<Craftsman(id={sample_craftsman.id}, name='Test Craftsman', specialties='carpentry,plumbing')>"
        assert repr(sample_craftsman) == expected


class TestProjectModel:
    """Test Project model functionality."""

    def test_create_project(self, db_session, sample_user, sample_client):
        """Test creating a project."""
        project = Project(
            name="Test Project",
            description="A test project",
            status=ProjectStatus.PLANNING,
            budget=Decimal("5000.00"),
            start_date=date(2024, 1, 1),
            user_id=sample_user.id,
            client_id=sample_client.id,
        )
        db_session.add(project)
        db_session.commit()

        assert project.id is not None
        assert project.name == "Test Project"
        assert project.status == ProjectStatus.PLANNING
        assert project.budget == Decimal("5000.00")
        assert project.user_id == sample_user.id
        assert project.client_id == sample_client.id
        assert project.created_at is not None

    def test_project_relationships(self, db_session, sample_user, sample_client):
        """Test project relationships."""
        project = Project(
            name="Relationship Test",
            status=ProjectStatus.ACTIVE,
            user_id=sample_user.id,
            client_id=sample_client.id,
        )
        db_session.add(project)
        db_session.commit()
        db_session.refresh(project)

        # Test relationships
        assert project.user == sample_user
        assert project.client == sample_client
        assert project in sample_user.projects
        assert project in sample_client.projects


class TestCampaignModel:
    """Test Campaign model functionality."""

    def test_create_campaign(self, db_session, sample_user, sample_client):
        """Test creating a campaign."""
        project = Project(
            name="Test Project",
            status=ProjectStatus.ACTIVE,
            user_id=sample_user.id,
            client_id=sample_client.id,
        )
        db_session.add(project)
        db_session.commit()

        campaign = Campaign(
            name="Test Campaign",
            description="A test campaign",
            status=CampaignStatus.ACTIVE,
            project_id=project.id,
        )
        db_session.add(campaign)
        db_session.commit()

        assert campaign.id is not None
        assert campaign.name == "Test Campaign"
        assert campaign.status == CampaignStatus.ACTIVE
        assert campaign.project_id == project.id
        assert campaign.created_at is not None


class TestItemModel:
    """Test Item model functionality."""

    def test_create_item(self, db_session, sample_user, sample_client):
        """Test creating an item."""
        project = Project(
            name="Test Project",
            status=ProjectStatus.ACTIVE,
            user_id=sample_user.id,
            client_id=sample_client.id,
        )
        db_session.add(project)
        db_session.commit()

        campaign = Campaign(
            name="Test Campaign", status=CampaignStatus.ACTIVE, project_id=project.id
        )
        db_session.add(campaign)
        db_session.commit()

        item = Item(
            name="Test Item",
            description="A test item",
            quantity=10,
            unit=Unit.UNIT,
            estimated_cost=Decimal("100.00"),
            campaign_id=campaign.id,
        )
        db_session.add(item)
        db_session.commit()

        assert item.id is not None
        assert item.name == "Test Item"
        assert item.quantity == 10
        assert item.unit == Unit.UNIT
        assert item.estimated_cost == Decimal("100.00")
        assert item.campaign_id == campaign.id


class TestQuoteModel:
    """Test Quote model functionality."""

    def test_create_quote(
        self, db_session, sample_user, sample_client, sample_craftsman
    ):
        """Test creating a quote."""
        project = Project(
            name="Test Project",
            status=ProjectStatus.ACTIVE,
            user_id=sample_user.id,
            client_id=sample_client.id,
        )
        db_session.add(project)
        db_session.commit()

        campaign = Campaign(
            name="Test Campaign", status=CampaignStatus.ACTIVE, project_id=project.id
        )
        db_session.add(campaign)
        db_session.commit()

        item = Item(
            name="Test Item", quantity=5, unit=Unit.HOUR, campaign_id=campaign.id
        )
        db_session.add(item)
        db_session.commit()

        quote = Quote(
            price=Decimal("150.00"),
            currency=Currency.EUR,
            description="Quote for test item",
            status=QuoteStatus.PENDING,
            margin_percentage=Decimal("20.00"),
            valid_until=date(2024, 12, 31),
            item_id=item.id,
            craftsman_id=sample_craftsman.id,
        )
        db_session.add(quote)
        db_session.commit()

        assert quote.id is not None
        assert quote.price == Decimal("150.00")
        assert quote.currency == Currency.EUR
        assert quote.status == QuoteStatus.PENDING
        assert quote.margin_percentage == Decimal("20.00")
        assert quote.item_id == item.id
        assert quote.craftsman_id == sample_craftsman.id


class TestTaskModel:
    """Test Task model functionality."""

    def test_create_task(self, db_session, sample_user, sample_client):
        """Test creating a task."""
        project = Project(
            name="Test Project",
            status=ProjectStatus.ACTIVE,
            user_id=sample_user.id,
            client_id=sample_client.id,
        )
        db_session.add(project)
        db_session.commit()

        task = Task(
            title="Test Task",
            description="A test task",
            status=TaskStatus.TODO,
            priority=TaskPriority.MEDIUM,
            due_date=date(2024, 6, 1),
            project_id=project.id,
            assigned_user_id=sample_user.id,
        )
        db_session.add(task)
        db_session.commit()

        assert task.id is not None
        assert task.title == "Test Task"
        assert task.status == TaskStatus.TODO
        assert task.priority == TaskPriority.MEDIUM
        assert task.project_id == project.id
        assert task.assigned_user_id == sample_user.id


class TestEnums:
    """Test enum values."""

    def test_project_status_enum(self):
        """Test ProjectStatus enum values."""
        assert ProjectStatus.PLANNING == "planning"
        assert ProjectStatus.ACTIVE == "active"
        assert ProjectStatus.COMPLETED == "completed"
        assert ProjectStatus.CANCELLED == "cancelled"
        assert ProjectStatus.ON_HOLD == "on hold"

    def test_campaign_status_enum(self):
        """Test CampaignStatus enum values."""
        assert CampaignStatus.ACTIVE == "active"
        assert CampaignStatus.COMPLETED == "completed"
        assert CampaignStatus.CANCELLED == "cancelled"
        assert CampaignStatus.ON_HOLD == "on hold"

    def test_quote_status_enum(self):
        """Test QuoteStatus enum values."""
        assert QuoteStatus.PENDING == "pending"
        assert QuoteStatus.APPROVED == "approved"
        assert QuoteStatus.REJECTED == "rejected"
        assert QuoteStatus.EXPIRED == "expired"

    def test_currency_enum(self):
        """Test Currency enum values."""
        assert Currency.EUR == "EUR"
        assert Currency.USD == "USD"
        assert Currency.GBP == "GBP"

    def test_unit_enum(self):
        """Test Unit enum values."""
        assert Unit.UNIT == "unit"
        assert Unit.HOUR == "hour"
        assert Unit.SQUARE_METER == "square meter"
        assert Unit.LINEAR_METER == "linear meter"
        assert Unit.KILOGRAM == "kilogram"
        assert Unit.CUBIC_METER == "cubic meter"
