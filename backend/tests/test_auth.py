"""Tests for authentication endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_success(client: AsyncClient):
    """TC-01: Valid registration returns 200 with user_id."""
    resp = await client.post("/auth/register", json={
        "name": "Alice",
        "email": "alice@example.com",
        "password": "Alice@1234",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert "user_id" in data
    assert data["role"] == "attendee"


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient):
    """TC-02: Duplicate email returns 400."""
    payload = {"name": "Bob", "email": "bob@example.com", "password": "Bob@1234"}
    await client.post("/auth/register", json=payload)
    resp = await client.post("/auth/register", json=payload)
    assert resp.status_code == 400
    assert "already registered" in resp.json()["detail"].lower()


@pytest.mark.asyncio
async def test_register_admin_blocked(client: AsyncClient):
    """TC-03: Attempting to register as ADMIN is blocked with 403."""
    resp = await client.post("/auth/register", json={
        "name": "Hacker",
        "email": "hacker@example.com",
        "password": "Hack@1234",
        "role": "ADMIN",
    })
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_register_weak_password(client: AsyncClient):
    """TC-04: Weak password is rejected with 422."""
    resp = await client.post("/auth/register", json={
        "name": "Weak",
        "email": "weak@example.com",
        "password": "password",  # no uppercase, digit, special char
    })
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, registered_user):
    """TC-05: Valid login returns access_token."""
    resp = await client.post("/auth/login", json={
        "email": registered_user["email"],
        "password": registered_user["password"],
    })
    assert resp.status_code == 200
    assert "access_token" in resp.json()
    assert resp.json()["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient, registered_user):
    """TC-06: Wrong password returns 401."""
    resp = await client.post("/auth/login", json={
        "email": registered_user["email"],
        "password": "WrongPass@999",
    })
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_login_unknown_email(client: AsyncClient):
    """TC-07: Unknown email returns 401."""
    resp = await client.post("/auth/login", json={
        "email": "nobody@example.com",
        "password": "Any@1234",
    })
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_get_me(client: AsyncClient, auth_headers):
    """TC-08: /auth/me returns current user payload from JWT."""
    resp = await client.get("/auth/me", headers=auth_headers)
    assert resp.status_code == 200
    assert "email" in resp.json()


@pytest.mark.asyncio
async def test_get_me_unauthenticated(client: AsyncClient):
    """TC-09: /auth/me without token returns 401."""
    resp = await client.get("/auth/me")
    assert resp.status_code == 401
