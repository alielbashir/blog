import asyncio
from typing import Iterator

import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from decouple import config
from fastapi import FastAPI
from httpx import AsyncClient

from src.config import CONFIG

# Override config settings before loading the app
CONFIG.testing = True
CONFIG.mongo_uri = config("TEST_MONGO_URI", default="mongodb://localhost:27017")

from src.main import app  # noqa: E402


async def clear_database(server: FastAPI) -> None:
    """Empties the test database"""
    print(f"clearing db with name {server.db.name}")
    for collection in await server.db.list_collections():
        await server.db[collection["name"]].delete_many({})


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest_asyncio.fixture(scope="session")
async def client() -> Iterator[AsyncClient]:
    """Async server client that handles lifespan and teardown"""
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test") as _client:
            try:
                yield _client
            except Exception as exc:
                print(exc)
            finally:
                await clear_database(app)
