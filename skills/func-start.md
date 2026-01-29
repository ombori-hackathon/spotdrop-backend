# Func-Start Skill

Start the backend development server.

## Usage

```
/func-start
```

## Commands

```bash
cd spotdrop-backend
uvicorn src.main:app --reload --port 8000
```

## What it does

1. Starts FastAPI with hot reload enabled
2. Server runs on http://localhost:8000
3. API docs available at http://localhost:8000/docs

## Prerequisites

- Docker containers running (PostgreSQL, MinIO)
- Dependencies installed (`/build`)
- Migrations applied (`alembic upgrade head`)
