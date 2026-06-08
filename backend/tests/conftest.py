"""Pytest configuration and shared fixtures for EventPulse test suite."""

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
import os

os.environ.setdefault("SECRET_KEY", "test-secret-key-eventpulse-ci")
os.environ.setdefault("MONGODB_URI", "mongodb://localhost:27017/eventpulse_test")
os.environ.setdefault(
    "DATABASE_URL",
    "postgresql+asyncpg://testuser:testpassword@localhost:5432/eventpulse_test"
)

from app.main import app
from app.database.postgres import Base, get_db
from app.auth.security import hash_password

# ── In-memory async engine for tests ─────────────────────────────────────────
TEST_DATABASE_URL = os.environ["DATABASE_URL"]

test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestSessionLocal = async_sessionmaker(
    bind=test_engine, class_=AsyncSession, expire_on_commit=False
)


async def override_get_db():
    async with TestSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_database():
    """Create all tables once before the test session."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client():
    """Async HTTP test client."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest_asyncio.fixture
async def db_session():
    """Isolated DB session for each test."""
    async with TestSessionLocal() as session:
        yield session


@pytest_asyncio.fixture
async def registered_user(client: AsyncClient):
    """Register a test user and return credentials."""
    payload = {
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "Test@1234",
    }
    await client.post("/auth/register", json=payload)
    return payload


@pytest_asyncio.fixture
async def auth_token(client: AsyncClient, registered_user):
    """Login and return a valid JWT token."""
    resp = await client.post(
        "/auth/login",
        json={
            "email": registered_user["email"],
            "password": registered_user["password"],
        },
    )
    return resp.json().get("access_token", "")


@pytest_asyncio.fixture
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}
