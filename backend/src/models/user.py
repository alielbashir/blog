from beanie import Document
from pydantic import BaseModel


class UserAuth(BaseModel):
    username: str
    password: str


class User(Document):
    username: str
    password: str


class UserOut(BaseModel):
    username: str
