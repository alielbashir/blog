import random
from beanie import init_beanie
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient

from src.config import CONFIG
from src.models.post import Post
from src.models.user import User

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def init_app():
    def random_str():
        """create random string to prevent collisions during parallel testing"""
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        return "".join(random.choices(alphabet, k=8))

    # FIXME: change config in the future
    dbname = random_str() if CONFIG.testing else "prod"
    print(f"dbname = {dbname}")
    print(f"config testing = {CONFIG.testing}")
    app.db = AsyncIOMotorClient(CONFIG.mongo_uri)[dbname]

    await init_beanie(app.db, document_models=[User, Post])


@app.get("/")
async def hello_world():
    return {"message": "Hello World"}
