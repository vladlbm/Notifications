import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from tortoise import Tortoise
from main import app


@pytest_asyncio.fixture(autouse=True)
async def init_db():
    await Tortoise.init(
        db_url="sqlite://:memory:",
        modules={"models": [
                     "app.models.user",
                     "app.models.notification"
            ]
        }
    )
    await Tortoise.generate_schemas()

    yield

    await Tortoise.close_connections()


@pytest_asyncio.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client