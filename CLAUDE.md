# SpotDrop Backend

Python FastAPI REST API for the SpotDrop platform.

## Tech Stack

- **Framework:** FastAPI
- **Database:** PostgreSQL with SQLAlchemy 2.0
- **Migrations:** Alembic
- **Auth:** JWT (access + refresh tokens)
- **Storage:** MinIO (S3-compatible)
- **Validation:** Pydantic v2

## Project Structure

```
spotdrop-backend/
├── src/
│   ├── main.py              # FastAPI app entry point
│   ├── api/
│   │   ├── deps.py          # Dependency injection (get_current_user, get_db)
│   │   └── routes/          # API route handlers (one file per resource)
│   │       ├── auth.py      # /api/auth/* endpoints
│   │       ├── users.py     # /api/users/* endpoints
│   │       └── spots.py     # /api/spots/* endpoints
│   ├── core/
│   │   ├── config.py        # Pydantic Settings from environment
│   │   ├── security.py      # JWT creation/validation, password hashing
│   │   └── exceptions.py    # Custom HTTP exceptions
│   ├── db/
│   │   ├── base.py          # SQLAlchemy DeclarativeBase
│   │   └── session.py       # Database engine and session factory
│   ├── models/              # SQLAlchemy ORM models (one file per entity)
│   │   ├── user.py
│   │   ├── spot.py
│   │   └── image.py
│   ├── schemas/             # Pydantic validation schemas (one file per resource)
│   │   ├── user.py          # UserCreate, UserResponse, TokenResponse
│   │   ├── spot.py          # SpotCreate, SpotUpdate, SpotResponse
│   │   └── image.py         # ImageCreate, ImageResponse
│   └── services/            # Business logic layer (one file per domain)
│       ├── spots.py         # SpotService class
│       ├── storage.py       # StorageService (MinIO)
│       └── geocoding.py     # GeocodingService (Nominatim)
├── alembic/                 # Database migrations
│   ├── versions/            # Migration files (001_initial.py, etc.)
│   ├── env.py
│   └── script.py.mako
├── tests/                   # Unit tests (mirror src structure)
│   ├── conftest.py          # Fixtures: db, client, test_user, auth_headers
│   ├── test_auth.py
│   ├── test_spots.py
│   └── test_users.py
├── agents/                  # Agent role definitions
├── skills/                  # Skill definitions
└── pyproject.toml           # Dependencies and configuration
```

## Structure Requirements (MUST FOLLOW)

When adding new features, you MUST follow these patterns:

### Adding a New Resource (e.g., "comments")

1. **Model** - Create `src/models/comment.py`:
   ```python
   from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
   from sqlalchemy.orm import relationship
   from src.db.base import Base
   import datetime

   class Comment(Base):
       __tablename__ = "comments"

       id = Column(Integer, primary_key=True, index=True)
       content = Column(String, nullable=False)
       user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
       spot_id = Column(Integer, ForeignKey("spots.id", ondelete="CASCADE"))
       created_at = Column(DateTime, default=datetime.datetime.utcnow)

       user = relationship("User", back_populates="comments")
       spot = relationship("Spot", back_populates="comments")
   ```

2. **Schema** - Create `src/schemas/comment.py`:
   ```python
   from pydantic import BaseModel, Field
   from datetime import datetime

   class CommentCreate(BaseModel):
       content: str = Field(..., min_length=1, max_length=500)
       spot_id: int

   class CommentResponse(BaseModel):
       id: int
       content: str
       user_id: int
       spot_id: int
       created_at: datetime

       model_config = {"from_attributes": True}
   ```

3. **Service** - Create `src/services/comments.py`:
   ```python
   from sqlalchemy.ext.asyncio import AsyncSession
   from src.models.comment import Comment
   from src.schemas.comment import CommentCreate

   class CommentService:
       async def create(self, db: AsyncSession, comment_in: CommentCreate, user_id: int) -> Comment:
           comment = Comment(**comment_in.model_dump(), user_id=user_id)
           db.add(comment)
           await db.commit()
           await db.refresh(comment)
           return comment

   comment_service = CommentService()
   ```

4. **Route** - Create `src/api/routes/comments.py`:
   ```python
   from fastapi import APIRouter, Depends
   from sqlalchemy.ext.asyncio import AsyncSession
   from src.api.deps import get_db, get_current_user
   from src.schemas.comment import CommentCreate, CommentResponse
   from src.services.comments import comment_service

   router = APIRouter(prefix="/api/comments", tags=["comments"])

   @router.post("", response_model=CommentResponse, status_code=201)
   async def create_comment(
       comment_in: CommentCreate,
       db: AsyncSession = Depends(get_db),
       current_user = Depends(get_current_user),
   ):
       return await comment_service.create(db, comment_in, current_user.id)
   ```

5. **Register Router** - Add to `src/main.py`:
   ```python
   from src.api.routes import comments
   app.include_router(comments.router)
   ```

6. **Migration** - Create migration in `alembic/versions/`:
   ```bash
   alembic revision --autogenerate -m "add_comments_table"
   ```

7. **Tests** - Create `tests/test_comments.py`

### Key Patterns

| Layer | Location | Pattern |
|-------|----------|---------|
| Routes | `src/api/routes/*.py` | Thin handlers, delegate to services |
| Services | `src/services/*.py` | All business logic, async methods |
| Models | `src/models/*.py` | SQLAlchemy ORM, relationships |
| Schemas | `src/schemas/*.py` | Pydantic v2, `*Create`, `*Update`, `*Response` |
| Deps | `src/api/deps.py` | Shared dependencies (auth, db session) |
| Config | `src/core/config.py` | Environment-based settings |
| Exceptions | `src/core/exceptions.py` | Custom HTTP exceptions |

### Naming Conventions

- **Files:** lowercase with underscores (`spot_service.py`)
- **Classes:** PascalCase (`SpotService`)
- **Functions:** lowercase with underscores (`create_spot`)
- **Schema Suffixes:** `*Create`, `*Update`, `*Response`
- **Route Prefixes:** `/api/<resource>` (e.g., `/api/spots`)

## Quick Start

```bash
# Install dependencies
pip install -e ".[dev]"

# Set up environment
cp .env.example .env

# Run migrations
alembic upgrade head

# Start server
uvicorn src.main:app --reload --port 8000
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/auth/register | Register new user |
| POST | /api/auth/login | Login and get tokens |
| POST | /api/auth/refresh | Refresh access token |
| GET | /api/users/me | Get current user |
| PATCH | /api/users/me | Update current user |
| POST | /api/spots | Create a spot |
| GET | /api/spots | List spots (with filters) |
| GET | /api/spots/{id} | Get spot details |
| PATCH | /api/spots/{id} | Update spot |
| DELETE | /api/spots/{id} | Delete spot |
| POST | /api/spots/{id}/images | Upload images |
| DELETE | /api/images/{id} | Delete image |

## Environment Variables

See `.env.example` for all required variables.

## Testing

```bash
pytest tests/ -v
```

## Agents

- `@architect` - API design, database schema, auth flow
- `@developer` - Routes, services, models implementation
- `@debugger` - API debugging, database issues
- `@reviewer` - Code review

## Skills

- `/build` - Install dependencies
- `/func-start` - Start development server
- `/lint` - Run ruff linter
- `/test` - Run pytest
