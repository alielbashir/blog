from fastapi import APIRouter
from src.auth import AuthHandler

# FIXME: consider way to have this as singleton and not instantiate every time in different files
auth_handler = AuthHandler()

router = APIRouter(prefix="/posts")
