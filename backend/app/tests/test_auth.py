import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings

client = TestClient(app)

def test_login_demo_investigator_success():
    payload = {
        "username": settings.DEMO_USERNAME,
        "password": settings.DEMO_PASSWORD
    }
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["username"] == settings.DEMO_USERNAME
    assert data["user"]["email"] == settings.DEMO_EMAIL

def test_login_invalid_password():
    payload = {
        "username": settings.DEMO_USERNAME,
        "password": "WrongPassword123!"
    }
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 401
    assert "Invalid username/email or password" in response.json()["detail"]

def test_login_unknown_user():
    payload = {
        "username": "nonexistent_user_999",
        "password": "Password123!"
    }
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 401

def test_get_me_unauthenticated():
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401

def test_get_me_authenticated():
    # 1. Login to get token
    login_res = client.post("/api/v1/auth/login", json={
        "username": settings.DEMO_USERNAME,
        "password": settings.DEMO_PASSWORD
    })
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]

    # 2. Fetch /me with Bearer token header
    headers = {"Authorization": f"Bearer {token}"}
    me_res = client.get("/api/v1/auth/me", headers=headers)
    assert me_res.status_code == 200
    user_data = me_res.json()
    assert user_data["username"] == settings.DEMO_USERNAME
    assert user_data["email"] == settings.DEMO_EMAIL
    assert user_data["is_active"] is True

import uuid

def test_register_new_user_success():
    unique_id = uuid.uuid4().hex[:6]
    new_user_payload = {
        "username": f"investigator_{unique_id}",
        "email": f"john_{unique_id}@chainsentinel.gov",
        "password": "SecurePassword2026!",
        "full_name": "John Doe",
        "role": "analyst"
    }
    res = client.post("/api/v1/auth/register", json=new_user_payload)
    assert res.status_code == 201
    data = res.json()
    assert data["username"] == f"investigator_{unique_id}"
    assert data["email"] == f"john_{unique_id}@chainsentinel.gov"
    assert "password_hash" not in data

def test_register_duplicate_username():
    new_user_payload = {
        "username": settings.DEMO_USERNAME,
        "email": "unique_email@chainsentinel.gov",
        "password": "SecurePassword2026!",
        "full_name": "Duplicate User"
    }
    res = client.post("/api/v1/auth/register", json=new_user_payload)
    assert res.status_code == 409

def test_logout_endpoint():
    login_res = client.post("/api/v1/auth/login", json={
        "username": settings.DEMO_USERNAME,
        "password": settings.DEMO_PASSWORD
    })
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    logout_res = client.post("/api/v1/auth/logout", headers=headers)
    assert logout_res.status_code == 200
