from __future__ import annotations
import os, sys, uuid, pathlib, subprocess, urllib.parse

os.environ["DATABASE_URL"] = "postgresql+asyncpg://postgres:postgres@localhost:6543/travel_wallet_test"
os.environ["MODE"] = "test"
os.environ.setdefault("SECRET_KEY", "tests-secret")


project_root = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))


import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import pytest
from sqlalchemy import create_engine, inspect
from app.models.base import Base  # ← your declarative base

@pytest.fixture(scope="session", autouse=True)
def _prepare_database():
    """Prepare test DB schema using sync engine and Alembic."""
    async_url = os.environ["DATABASE_URL"]
    alembic_url = async_url.replace("+asyncpg", "+psycopg2")
    plain_url = async_url.replace("+asyncpg", "")

    parsed = urllib.parse.urlparse(plain_url)
    admin_url = parsed._replace(path="/postgres").geturl()
    db_name = parsed.path.lstrip("/")

    # Create DB if it doesn't exist
    try:
        conn = psycopg2.connect(admin_url)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        with conn.cursor() as cur:
            cur.execute(f'CREATE DATABASE "{db_name}"')
    except psycopg2.errors.DuplicateDatabase:
        pass
    finally:
        if "conn" in locals():
            conn.close()

    # Run Alembic migrations
    result = subprocess.run(
        ["alembic", "upgrade", "head"],
        cwd=project_root,
        env={**os.environ, "DATABASE_URL": alembic_url},
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print("--- Alembic stdout ---\n", result.stdout)
        print("--- Alembic stderr ---\n", result.stderr)
        raise RuntimeError("Alembic migration failed")

    engine = create_engine(plain_url)
    insp = inspect(engine)
    missing = [t for t in Base.metadata.tables if not insp.has_table(t)]
    if missing:
        Base.metadata.create_all(engine, tables=[Base.metadata.tables[n] for n in missing])

# Clear config settings
from core.config import get_settings
get_settings.cache_clear()

# Test client/db
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession
from main import app
from app.db.session import async_session_maker, get_db

def pytest_configure(config):
    config.addinivalue_line("markers", "asyncio")

from typing import AsyncGenerator

@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Yield a clean AsyncSession for each test (no SAVEPOINTs)."""
    async with async_session_maker() as session:
        yield session
        await session.close()

@pytest_asyncio.fixture(scope="function")
async def async_client():
    """Yield an HTTPX AsyncClient with isolated DB session per request."""
    async def _override_get_db():
        async with async_session_maker() as session:
            yield session

    app.dependency_overrides[get_db] = _override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()

# register fake user
async def get_auth_header(client) -> dict[str, str]:
    email = f"test_{uuid.uuid4().hex}@example.com"
    payload = {"email": email, "password": "Pass123!", "full_name": "Test User"}
    r = await client.post("/auth/register", json=payload)
    assert r.status_code in (200, 201)
    return {"Authorization": f"Bearer {r.json()['access_token']}"}
