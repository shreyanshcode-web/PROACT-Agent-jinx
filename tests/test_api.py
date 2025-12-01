import sys
import os
import pytest
import tempfile

# Add project root to path so backend is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.fixture
def temp_db():
    """Create a temporary SQLite DB file for each test."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_file = os.path.join(tmpdir, "test.db")
        db_url = f"sqlite:///{db_file}"
        yield db_url

def test_signup_and_login(temp_db, monkeypatch):
    """Test signup and login with bcrypt hashing using sync TestClient."""
    # Set DB URL before importing app
    monkeypatch.setenv("JINX_DATABASE_URL", temp_db)
    
    # Import here after env is set
    import importlib
    from backend import api_server
    importlib.reload(api_server)  # Reload to pick up new DB URL
    from fastapi.testclient import TestClient

    client = TestClient(api_server.app)

    # Signup
    r = client.post("/api/signup", json={"username": "testuser", "password": "pwd123"})
    assert r.status_code == 200
    data = r.json()
    assert data.get("status") == "created"

    # Duplicate signup should fail
    r2 = client.post("/api/signup", json={"username": "testuser", "password": "pwd123"})
    assert r2.status_code == 400

    # Login with correct credentials
    r3 = client.post("/api/login", json={"username": "testuser", "password": "pwd123"})
    assert r3.status_code == 200
    assert r3.json().get("token") == "testuser"

    # Login with wrong password
    r4 = client.post("/api/login", json={"username": "testuser", "password": "wrong"})
    assert r4.status_code == 401
