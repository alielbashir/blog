from beanie import init_beanie
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from src.config import CONFIG
from src.models.post import Post
from src.models.user import User

app = FastAPI()


@app.on_event("startup")
async def init_app():
    # FIXME: change config in the future
    dbname = "test" if CONFIG.testing else "prod"
    print(f"dbname = {dbname}")
    print(f"config testing = {CONFIG.testing}")
    app.db = AsyncIOMotorClient(CONFIG.mongo_uri)[dbname]

    await init_beanie(app.db, document_models=[User, Post])


@app.get("/")
async def hello_world():
    return {"message": "Hello World"}
