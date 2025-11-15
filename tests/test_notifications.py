import pytest
import pytest_asyncio
from httpx import AsyncClient
from main import app

pytestmark = pytest.mark.asyncio

async def test_notifications_crud(async_client: AsyncClient):
    # Регистрация пользователя
    register_payload = {"username": "testuser", "password": "password123"}
    response = await async_client.post("/auth/register", json=register_payload)
    assert response.status_code == 200
    data = response.json()
    access_token = data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    # Создание уведомления
    create_payload = {"type": "like", "text": "Test notification"}
    response = await async_client.post("/notifications/", json=create_payload, headers=headers)
    assert response.status_code == 200
    notification = response.json()
    assert notification["text"] == "Test notification"
    assert notification["type"] == "like"
    assert notification["username"] == "testuser"

    notification_id = notification["id"]

    # Получение уведомления
    response = await async_client.get("/notifications/?limit=10&offset=0", headers=headers)
    assert response.status_code == 200
    notifications_list = response.json()
    assert any(n["id"] == notification_id for n in notifications_list)

    # Удаление уведомления
    response = await async_client.delete(f"/notifications/{notification_id}", headers=headers)
    assert response.status_code == 204

    # Проверка на удалеие
    response = await async_client.get("/notifications/?limit=10&offset=0", headers=headers)
    assert response.status_code == 200
    notifications_list = response.json()
    assert all(n["id"] != notification_id for n in notifications_list)