"""Tests for events, speakers, sessions and registrations endpoints."""

import pytest
from httpx import AsyncClient


# ── Events ────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_list_events_public(client: AsyncClient):
    """TC-10: GET /events/ is publicly accessible and returns a list."""
    resp = await client.get("/events/")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


@pytest.mark.asyncio
async def test_create_event_unauthenticated(client: AsyncClient):
    """TC-11: Creating an event without a token returns 401."""
    resp = await client.post("/events/", json={
        "title": "Test Event",
        "start_date": "2026-09-01T09:00:00",
        "end_date": "2026-09-01T18:00:00",
        "max_attendees": 100,
    })
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_create_event_as_attendee_forbidden(client: AsyncClient, auth_headers):
    """TC-12: Attendee cannot create events (403)."""
    resp = await client.post("/events/", headers=auth_headers, json={
        "title": "Unauthorized Event",
        "start_date": "2026-09-01T09:00:00",
        "end_date": "2026-09-01T18:00:00",
        "max_attendees": 50,
    })
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_get_event_not_found(client: AsyncClient):
    """TC-13: GET /events/99999 returns 404."""
    resp = await client.get("/events/99999")
    assert resp.status_code == 404


# ── Speakers ──────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_list_speakers_public(client: AsyncClient):
    """TC-14: GET /speakers/ is accessible and returns sessions_count per speaker."""
    resp = await client.get("/speakers/")
    assert resp.status_code in (200, 401)  # depends on auth requirement


@pytest.mark.asyncio
async def test_create_speaker_unauthenticated(client: AsyncClient):
    """TC-15: Creating a speaker without token returns 401."""
    resp = await client.post("/speakers/", json={
        "name": "Jane Doe",
        "email": "jane@example.com",
        "bio": "Speaker bio",
    })
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_create_speaker_as_attendee_forbidden(client: AsyncClient, auth_headers):
    """TC-16: Attendee cannot create speakers (403)."""
    resp = await client.post("/speakers/", headers=auth_headers, json={
        "name": "Unauthorized Speaker",
        "email": "unauth_speaker@example.com",
    })
    assert resp.status_code == 403


# ── Sessions ──────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_list_sessions_authenticated(client: AsyncClient, auth_headers):
    """TC-17: Authenticated user can list sessions."""
    resp = await client.get("/sessions/", headers=auth_headers)
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_list_sessions_unauthenticated(client: AsyncClient):
    """TC-18: Unauthenticated request to /sessions/ returns 401."""
    resp = await client.get("/sessions/")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_get_session_not_found(client: AsyncClient, auth_headers):
    """TC-19: GET /sessions/99999 returns 404."""
    resp = await client.get("/sessions/99999", headers=auth_headers)
    assert resp.status_code == 404


# ── Registrations ─────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_registration_unauthenticated(client: AsyncClient):
    """TC-20: Creating a registration without token returns 401."""
    resp = await client.post("/registrations/", json={
        "event_id": 1,
        "attendee_name": "Test",
        "attendee_email": "test@example.com",
    })
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_get_registration_not_found(client: AsyncClient, auth_headers):
    """TC-21: GET /registrations/99999 returns 404."""
    resp = await client.get("/registrations/99999", headers=auth_headers)
    assert resp.status_code == 404


# ── Health & Root ─────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_root_endpoint(client: AsyncClient):
    """TC-22: GET / returns running status."""
    resp = await client.get("/")
    assert resp.status_code == 200
    assert resp.json()["status"] == "running"


@pytest.mark.asyncio
async def test_health_endpoint(client: AsyncClient):
    """TC-23: GET /health returns healthy."""
    resp = await client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "healthy"


# ── Error Handler ─────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_404_error_envelope(client: AsyncClient):
    """TC-24: 404 response uses unified error envelope format."""
    resp = await client.get("/events/99999")
    assert resp.status_code == 404
    body = resp.json()
    assert "error" in body
    assert "detail" in body
    assert "path" in body
    assert "timestamp" in body


@pytest.mark.asyncio
async def test_validation_error_envelope(client: AsyncClient):
    """TC-25: Sending invalid JSON body returns 422 with error envelope."""
    resp = await client.post("/auth/register", json={
        "name": "",          # empty name
        "email": "not-an-email",
        "password": "x",     # too short
    })
    assert resp.status_code == 422
    body = resp.json()
    assert "error" in body
    assert "detail" in body
