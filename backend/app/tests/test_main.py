from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_root(client: AsyncClient) -> None:
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Hello World"
