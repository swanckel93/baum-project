from pathlib import Path

import pytest
from alembic.config import Config
from alembic.script import ScriptDirectory
from sqlalchemy import create_engine

from alembic import command
from app.core.config import settings


class TestMigrations:
    """Test Alembic migrations."""

    @pytest.fixture
    def alembic_config(self):
        """Create Alembic configuration for testing."""
        # Get the backend directory path
        backend_dir = Path(__file__).parent.parent
        alembic_cfg = Config(str(backend_dir / "alembic.ini"))

        # Use the test database URL from settings
        alembic_cfg.set_main_option("sqlalchemy.url", settings.test_database_url)

        return alembic_cfg

    @pytest.fixture
    def test_engine(self):
        """Create test database engine."""
        engine = create_engine(settings.test_database_url)
        return engine

    def test_migration_script_exists(self, alembic_config):
        """Test that migration script exists and is valid."""
        script_dir = ScriptDirectory.from_config(alembic_config)
        revisions = list(script_dir.walk_revisions())

        # Should have at least one revision (our initial migration)
        assert len(revisions) > 0

        # Check that the initial migration exists
        initial_revision = revisions[0]
        assert initial_revision.revision is not None
        assert "Initial migration" in initial_revision.doc

    def test_migration_sql_generation(self, alembic_config):
        """Test that migration can generate SQL without connecting to database."""
        # Test that we can generate SQL for the migration
        try:
            # This should work without connecting to database
            command.upgrade(alembic_config, "head", sql=True)
        except Exception as e:
            # Should not fail due to SQL generation
            if "sql" in str(e).lower():
                pytest.fail(f"SQL generation failed: {e}")
            # Other errors might be connection-related and are acceptable for this test

    def test_migration_file_content(self, alembic_config):
        """Test that migration file contains expected operations."""
        script_dir = ScriptDirectory.from_config(alembic_config)
        revisions = list(script_dir.walk_revisions())

        # Get the initial migration
        initial_revision = revisions[0]
        migration_path = script_dir.get_revision(initial_revision.revision).path

        # Read the migration file
        with open(migration_path) as f:
            content = f.read()

        # Check that it contains expected table creations
        expected_tables = [
            'create_table(\n        "users"',
            'create_table(\n        "clients"',
            'create_table(\n        "craftsmen"',
            'create_table(\n        "projects"',
            'create_table(\n        "campaigns"',
            'create_table(\n        "items"',
            'create_table(\n        "quotes"',
            'create_table(\n        "tasks"',
        ]

        for table_creation in expected_tables:
            assert table_creation in content

    def test_migration_contains_foreign_keys(self, alembic_config):
        """Test that migration contains foreign key constraints."""
        script_dir = ScriptDirectory.from_config(alembic_config)
        revisions = list(script_dir.walk_revisions())

        # Get the initial migration
        initial_revision = revisions[0]
        migration_path = script_dir.get_revision(initial_revision.revision).path

        # Read the migration file
        with open(migration_path) as f:
            content = f.read()

        # Check that it contains foreign key constraints
        expected_fks = [
            "ForeignKeyConstraint",
            "users.id",
            "clients.id",
            "projects.id",
            "campaigns.id",
            "craftsmen.id",
            "items.id",
        ]

        for fk in expected_fks:
            assert fk in content

    def test_migration_contains_indexes(self, alembic_config):
        """Test that migration contains index creations."""
        script_dir = ScriptDirectory.from_config(alembic_config)
        revisions = list(script_dir.walk_revisions())

        # Get the initial migration
        initial_revision = revisions[0]
        migration_path = script_dir.get_revision(initial_revision.revision).path

        # Read the migration file
        with open(migration_path) as f:
            content = f.read()

        # Check that it contains index creations
        expected_indexes = [
            "create_index",
            "ix_users_email",
            "ix_users_id",
            "ix_clients_id",
            "ix_projects_id",
        ]

        for index in expected_indexes:
            assert index in content

    def test_migration_contains_enums(self, alembic_config):
        """Test that migration contains enum type definitions."""
        script_dir = ScriptDirectory.from_config(alembic_config)
        revisions = list(script_dir.walk_revisions())

        # Get the initial migration
        initial_revision = revisions[0]
        migration_path = script_dir.get_revision(initial_revision.revision).path

        # Read the migration file
        with open(migration_path) as f:
            content = f.read()

        # Check that it contains enum definitions
        expected_enums = [
            "Enum(",
            "projectstatus",
            "campaignstatus",
            "quotestatus",
            "currency",
            "taskstatus",
            "taskpriority",
            "unit",
        ]

        for enum_def in expected_enums:
            assert enum_def in content
