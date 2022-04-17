from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_root(client: AsyncClient) -> None:
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Hello World"


# @pytest.mark.asyncio
# async def test_new_user(client: AsyncClient) -> None:
#     new_user = {"username": "jakeperalta", "password": "amysantiago"}
#     response = await client.post("/users/register", json=new_user)
#     assert response.status_code == 201
#     data = response.json()
#     assert data["username"] == "jakeperalta"

#     # check if user added to db
#     response = await client.post("/users/login", json=new_user)
#     assert response.status_code == 200
#     data = response.json()
#     assert "token" in data
