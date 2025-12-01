import os
import pytest


@pytest.mark.asyncio
async def test_signup_and_login(tmp_path, monkeypatch):
    # Use an in-memory sqlite DB for tests
    monkeypatch.setenv("JINX_DATABASE_URL", "sqlite:///:memory:")
    # Import app after env var is set so DB engine uses correct URL
    from backend import api_server
    from httpx import AsyncClient

    async with AsyncClient(app=api_server.app, base_url="http://test") as ac:
        # Signup
        r = await ac.post("/api/signup", json={"username": "testuser", "password": "s3cret"})
        assert r.status_code == 200
        data = r.json()
        assert data.get("status") == "created"

        # Duplicate signup should fail
        r2 = await ac.post("/api/signup", json={"username": "testuser", "password": "s3cret"})
        assert r2.status_code == 400

        # Login with correct credentials
        r3 = await ac.post("/api/login", json={"username": "testuser", "password": "s3cret"})
        assert r3.status_code == 200
        assert r3.json().get("token") == "testuser"

        # Login with wrong password
        r4 = await ac.post("/api/login", json={"username": "testuser", "password": "wrong"})
        assert r4.status_code == 401
