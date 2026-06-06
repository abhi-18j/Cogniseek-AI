OmniSearch — Backend (Phase 1)

Quick start:

1. Copy .env.example to backend/.env:
   cp backend/.env.example backend/.env

2. From project root (OMNIS) run:
   docker compose up --build

3. Open API docs:
   http://localhost:8000/docs

What is included:
- FastAPI app with health endpoint
- Async SQLAlchemy database layer foundations
- Alembic env.py scaffold for future migrations
- Centralized config and logging
- PostgreSQL in Docker

Notes:
- This phase does not implement models, migrations, or integrations.
- The backend performs a lightweight DB connectivity check on startup.
