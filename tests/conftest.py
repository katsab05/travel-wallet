"""
Global pytest fixtures   +   helper to register a throw-away user
-----------------------------------------------------------------
* Forces async DATABASE_URL to use +asyncpg
* Adds project root to PYTHONPATH
* Clears Settings cache so new env is seen
* Provides:
      db_session   – brand-new AsyncSession per test (no SAVEPOINT gymnastics)
      async_client – httpx.AsyncClient (ASGITransport) + dependency override
      get_auth_header(client) → {"Authorization": "Bearer <token>"}
"""

from __future__ import annotations
import os, sys, uuid
import subprocess, pytest
from pathlib import Path
from typing import AsyncGenerator

# ───────────── 1. patch env BEFORE imports ────────────── #
os.environ["DATABASE_URL"] = "postgresql+asyncpg://postgres:postgres@localhost:6543/travel_wallet_test"
os.environ.setdefault("MODE", "test")
os.environ.setdefault("SECRET_KEY", "tests-secret")

# add project root to PYTHONPATH so 'core', 'app' import
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

# ───────────── 2. clear Settings cache ────────────────── #
from core.config import get_settings          # noqa: E402
get_settings.cache_clear()

# ───────────── 3. import app / DB objects ─────────────── #
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession

from main import app
from app.db.session import async_session_maker, get_db

from sqlalchemy.ext.asyncio import create_async_engine

from app.models.base import Base


# pytest-asyncio marker auto-enable
def pytest_configure(config):
    config.addinivalue_line("markers", "asyncio")


# ─────────────  fixtures  ─────────────────────────────── #
import subprocess, pathlib, os, pytest

@pytest.fixture(scope="session", autouse=True)
def _apply_migrations():
    """
    Run Alembic once with a *sync* driver URL so tables
    (users, trips, expenses, …) are present for every test.
    """
    async_url = os.environ["DATABASE_URL"]
    sync_url = async_url.replace("+asyncpg", "+psycopg2")   # key line

    proj_root = pathlib.Path(__file__).resolve().parents[1]
    env = {**os.environ, "DATABASE_URL": sync_url}

    res = subprocess.run(
        ["alembic", "upgrade", "head"],
        cwd=proj_root,
        env=env,
        text=True,
        capture_output=True,
    )
    if res.returncode != 0:
        sys.stderr.write("\n--- Alembic stdout ---\n" + res.stdout)
        sys.stderr.write("\n--- Alembic stderr ---\n" + res.stderr)
        raise RuntimeError("Migrations did not apply - see logs above")
    

@pytest_asyncio.fixture(scope="session", autouse=True)
async def _ensure_all_tables():
    """Create any tables Alembic missed (dev safety-net)."""
    async_engine = create_async_engine(os.environ["DATABASE_URL"])
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Fresh AsyncSession per test.  No nested SAVEPOINT—services may commit.
    Test DB is disposable, so we don't roll back.
    """
    async with async_session_maker() as session:
        yield session
        await session.close()


@pytest_asyncio.fixture(scope="function")
async def async_client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """FastAPI test-client bound to the same DB session."""
    async def _override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db

    transport = ASGITransport(app=app)        # httpx ≥ 0.26
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()


# ─────────────  helper shared by all tests  ───────────── #
async def get_auth_header(client) -> dict[str, str]:
    """
    Register a unique user, return auth header.
    Guarantees no duplicate-email DB collisions.
    """
    email = f"test_{uuid.uuid4().hex}@example.com"
    payload = {"email": email, "password": "Pass123!", "full_name": "Test"}
    res = await client.post("/auth/register", json=payload)
    assert res.status_code in (200, 201)
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
