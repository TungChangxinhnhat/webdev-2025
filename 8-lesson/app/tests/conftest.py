import sys
import os
import pytest
from httpx import AsyncClient, ASGITransport

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app, users_db

@pytest.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest.fixture
async def auth_token(async_client):
    users_db.clear()
    
    user_data = {"username": "testuser", "password": "password123"}
    await async_client.post("/auth/register", json=user_data)
    
    response = await async_client.post("/auth/jwt/login", data=user_data)
    return response.json()["access_token"]

@pytest.fixture
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}