# Automated Testing

## Overview

A11y Workbench includes automated tests to ensure code quality and prevent regressions.

## Test Coverage

- **API Tests** (test_api.py) - HTTP endpoints
- **Repository Tests** (test_repositories.py) - Database operations  
- **Workflow Tests** (test_workflows.py) - End-to-end scenarios

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_api.py -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

## Test Database

Tests use a temporary SQLite database (`tests/test.db`) that is created and destroyed for each test, ensuring test isolation.

## Current Status

✅ 7 passing tests covering:
- Project creation and listing
- Target creation
- Issue creation and retrieval
- Multi-project workflows

## Adding Tests

1. Create test file in `tests/` directory
2. Import necessary modules
3. Write test functions starting with `test_`
4. Use pytest fixtures from `conftest.py`

Example:
```python
def test_create_project():
    response = client.post("/api/v1/projects", json={"name": "Test"})
    assert response.status_code == 200
    assert "id" in response.json()
```

## CI/CD Integration

Tests can be integrated into GitHub Actions or other CI/CD pipelines:

```yaml
- name: Run tests
  run: pytest tests/ -v
```
