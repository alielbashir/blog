from httpx import AsyncClient
import pytest

from src.models.user import Scope
from tests.utils import create_new_post, login_new_user


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


@pytest.mark.asyncio
async def test_create_new_post_with_permission(client: AsyncClient) -> None:
    """checks that a new post is created when a user with write scope performs it"""
    token = await login_new_user(client, username="rosadiaz", scope=Scope.write)

    response = await create_new_post(client, token)

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "test title"
    assert data["content"] == "test content"
    assert "id" in data


@pytest.mark.asyncio
async def test_create_new_post_without_permission(client: AsyncClient) -> None:
    """checks that a 403 error is returned when a user without write scope tries to create a new post"""
    token = await login_new_user(client, username="ginalinetti", scope=Scope.read)

    response = await create_new_post(client, token)

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_create_new_post_added_to_db(client: AsyncClient) -> None:
    """checks that new post is added to db when created"""
    token = await login_new_user(client, username="pontiacbandit", scope=Scope.write)

    response = await create_new_post(client, token)
    post_id = response.json()["id"]

    response = await client.get(
        f"/posts/{post_id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
