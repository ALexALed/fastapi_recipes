import pytest

from httpx import AsyncClient, ASGITransport
from ..main import app

@pytest.mark.asyncio
async def test_main():
    client = AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    )
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello World"
    }


async def test_read_main(test_client):
    response = await test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello World"
    }