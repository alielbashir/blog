from enum import Enum

from beanie import Document
from pydantic import BaseModel


class Scope(str, Enum):
    """Sope to control what a user is authorized to do"""

    read = "read"
    write = "write"


class UserAuth(BaseModel):
    username: str
    password: str


class UserRegister(UserAuth):
    scope: Scope = Scope.read


class User(Document):
    username: str
    password: str
    scope: Scope


class UserNoPass(BaseModel):
    """User without password"""

    username: str
    scope: Scope
