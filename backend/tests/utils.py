from httpx import AsyncClient, Response

from src.models.user import Scope


async def login_new_user(client: AsyncClient, username: str, scope: Scope) -> str:
    """Registers and logs in a new user and returns their token"""
    new_user = {"username": username, "password": "testpass", "scope": scope}
    response = await client.post("/users/register", json=new_user)

    data = response.json()

    new_user.pop("scope", None)

    response = await client.post("/users/login", json=new_user)
    data = response.json()
    return data["token"]


async def create_new_post(client: AsyncClient, token: str) -> Response:
    """Creates a new post and returns its response"""
    new_post = {"title": "Test Post", "content": "This is a test post."}
    response = await client.post(
        "/posts", json=new_post, headers={"Authorization": f"Bearer {token}"}
    )
    return response
