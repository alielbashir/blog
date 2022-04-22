from httpx import AsyncClient
import pytest

from src.models.user import Scope


@pytest.mark.asyncio
async def test_root(client: AsyncClient) -> None:
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Hello World"


@pytest.mark.asyncio
async def test_new_user_login(client: AsyncClient) -> None:
    new_user = {"username": "jakeperalta", "password": "amysantiago"}
    response = await client.post("/users/register", json=new_user)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "jakeperalta"

    # check if user added to db
    response = await client.post("/users/login", json=new_user)
    assert response.status_code == 200
    data = response.json()
    assert "token" in data

@pytest.mark.asyncio
async def test_new_user_with_default_scope(client: AsyncClient) -> None:
    """checks that scope defaults to read when not specified"""
    new_user = {"username": "terry", "password": "oldspice"}
    response = await client.post("/users/register", json=new_user)
    assert response.status_code == 201

    data = response.json()

    assert data["username"] == "terry"
    assert data["scope"] == Scope.read

@pytest.mark.asyncio
async def test_new_user_with_write_scope(client: AsyncClient) -> None:
    """checks that new user's scope is write when specified"""
    new_user = {"username": "captainholt", "password": "cheddar", "scope": "write"}
    response = await client.post("/users/register", json=new_user)
    assert response.status_code == 201

    data = response.json()

    assert data["username"] == "captainholt"
    assert data["scope"] == Scope.write
