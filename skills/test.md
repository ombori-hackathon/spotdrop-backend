# Test Skill

Run backend tests.

## Usage

```
/test
```

## Commands

```bash
cd spotdrop-backend
pytest tests/ -v
```

## Options

```bash
# Run with coverage
pytest tests/ -v --cov=src --cov-report=html

# Run specific test file
pytest tests/test_auth.py -v

# Run specific test
pytest tests/test_auth.py::test_login -v

# Run with debug output
pytest tests/ -v -s
```

## Prerequisites

- Docker containers running (PostgreSQL)
- Dependencies installed (`/build`)
