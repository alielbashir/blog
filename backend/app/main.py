from fastapi import FastAPI

from models.user import User
from config import CONFIG
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient


app = FastAPI()


@app.on_event("startup")
async def init_app():
    app.db = AsyncIOMotorClient(CONFIG.mongo_uri).account
    await init_beanie(app.db, document_models=[User])


@app.get("/")
async def root():
    return {"message": "Hello World"}
