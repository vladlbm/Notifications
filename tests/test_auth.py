import pytest
import pytest_asyncio
from httpx import AsyncClient
from main import app

pytestmark = pytest.mark.asyncio

async def test_register_login_refresh(async_client: AsyncClient):
    # Регистрация пользователя
    register_payload = {
        "username": "testuser",
        "password": "password123"
    }
    response = await async_client.post("/auth/register", json=register_payload)
    assert response.status_code == 200
    data = response.json()
    assert "user_id" in data
    assert "access_token" in data
    assert "refresh_token" in data

    access_token = data["access_token"]
    refresh_token = data["refresh_token"]

    # Логин
    login_payload = {
        "username": "testuser",
        "password": "password123"
    }
    response = await async_client.post(
        "/auth/login",
        data=login_payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data

    # Обновление access токена
    refresh_payload = {
        "refresh_token": refresh_token
    }
    response = await async_client.post("/auth/refresh", json=refresh_payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data