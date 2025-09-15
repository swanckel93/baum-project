# PostgreSQL Testing Setup

This document describes the PostgreSQL testing infrastructure implemented for the StudioHub backend.

## Overview

The testing system uses PostgreSQL instead of SQLite to ensure production-representative testing. Each test function gets its own isolated database that is created before the test runs and destroyed afterwards.

## Architecture

### Test Database Manager
- **Location**: `app/core/test_database.py`
- **Purpose**: Manages database lifecycle for isolated testing
- **Key Features**:
  - Creates unique database per test
  - Sets up schema using SQLAlchemy models
  - Cleans up after test completion
  - Handles connection management

### Configuration
- **Test Database**: Runs on port 5433 (separate from development)
- **Docker Container**: `studiohub-postgres-test`
- **Database Naming**: `test_{test_name}_{timestamp}_{uuid}`

## Setup Instructions

### 1. Start PostgreSQL Container
```bash
docker-compose -f docker-compose.test.yml up -d
```

### 2. Verify Connection
```bash
uv run python -c "from app.core.test_database import test_db_manager; print('✅ Connected!' if test_db_manager.verify_connection() else '❌ Failed!')"
```

### 3. Run Tests
```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/test_users_endpoints.py

# Run with coverage
uv run pytest --cov=app
```

## Test Database Lifecycle

Each test follows this lifecycle:

1. **Database Creation**: A unique database is created with format `test_{test_name}_{timestamp}_{uuid}`
2. **Schema Setup**: SQLAlchemy models create all tables
3. **Test Execution**: Test runs with isolated database session
4. **Cleanup**: Database is dropped after test completion

## Configuration Details

### Docker Compose Settings
```yaml
# docker-compose.test.yml
services:
  postgres-test:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: test_user
      POSTGRES_PASSWORD: test_password
      POSTGRES_DB: test_template
    ports:
      - "5433:5432"
```

### Application Settings
```python
# app/core/config.py
TEST_DB_HOST: str = "localhost"
TEST_DB_PORT: int = 5433
TEST_DB_USER: str = "test_user"
TEST_DB_PASSWORD: str = "test_password"
TEST_DB_NAME: str = "test_template"
```

## Benefits

### Production Parity
- Uses same database engine as production
- Catches PostgreSQL-specific issues
- Validates SQL dialect compatibility
- Tests foreign key constraints properly

### Test Isolation
- Each test gets fresh database
- No data leakage between tests
- Parallel test execution support
- Clean test environment

### Performance
- Fast database creation/deletion
- Optimized for CI/CD pipelines
- Efficient connection management
- Minimal resource usage

## CI/CD Integration

The system works seamlessly in GitHub Actions. The repository includes a complete CI workflow at `.github/workflows/ci.yml` that:

- Sets up PostgreSQL service on port 5433
- Installs Python 3.13 and uv package manager
- Runs linting with ruff
- Executes all tests with coverage reporting
- Uploads coverage results to Codecov

### GitHub Actions Configuration
```yaml
services:
  postgres:
    image: postgres:15-alpine
    env:
      POSTGRES_USER: test_user
      POSTGRES_PASSWORD: test_password
      POSTGRES_DB: test_template
    ports:
      - 5433:5432
    options: >-
      --health-cmd pg_isready
      --health-interval 10s
      --health-timeout 5s
      --health-retries 5
```

The workflow automatically:
1. Waits for PostgreSQL to be ready
2. Sets up the Python environment
3. Installs dependencies with uv
4. Runs linting checks
5. Executes all tests with PostgreSQL
6. Reports coverage metrics

## Troubleshooting

### Connection Issues
```bash
# Check if container is running
docker ps | grep postgres-test

# Check container logs
docker logs studiohub-postgres-test

# Test direct connection
psql -h localhost -p 5433 -U test_user -d test_template
```

### Performance Issues
- Monitor database creation/deletion times
- Check for leftover test databases
- Verify connection pool settings
- Monitor container resource usage

### Test Failures
- Check foreign key constraint errors (now properly enforced)
- Verify data types compatibility
- Review transaction handling
- Check concurrent access patterns

## Migration from SQLite

The migration from SQLite to PostgreSQL revealed several important differences:

1. **Foreign Key Constraints**: PostgreSQL enforces these strictly
2. **Data Types**: More precise type checking
3. **Transaction Handling**: Different behavior for rollbacks
4. **SQL Dialect**: PostgreSQL-specific features and syntax

## Future Improvements

1. **Database Pooling**: Implement connection pooling for better performance
2. **Parallel Testing**: Support for concurrent test execution
3. **Fixture Optimization**: Pre-populate common test data
4. **Performance Monitoring**: Track database creation/deletion times
5. **Error Handling**: Better handling of constraint violations in API layer

## Commands Reference

```bash
# Start test database
docker-compose -f docker-compose.test.yml up -d

# Stop test database
docker-compose -f docker-compose.test.yml down

# Clean volumes (fresh start)
docker-compose -f docker-compose.test.yml down -v

# Run tests with verbose output
uv run pytest -v

# Run tests with coverage report
uv run pytest --cov=app --cov-report=html

# Run specific test pattern
uv run pytest -k "test_create_user"
```

## Environment Variables

```bash
# Test Database Configuration
TEST_DB_HOST=localhost
TEST_DB_PORT=5433
TEST_DB_USER=test_user
TEST_DB_PASSWORD=test_password
TEST_DB_NAME=test_template
```

This PostgreSQL testing setup ensures that our tests run in an environment that closely matches production, helping us catch issues early and maintain high code quality.