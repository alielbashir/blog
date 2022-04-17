from fastapi import APIRouter, HTTPException
from core.auth import AuthHandler

from models.user import User, UserAuth, UserOut

auth_handler = AuthHandler()

router = APIRouter(prefix="/users")


@router.post("/register", status_code=201, response_model=UserOut)
async def register(user_auth: UserAuth):
    # TODO: #5 handle different privileges
    user = await User.find_one(User.username == user_auth.username)
    if user is not None:
        raise HTTPException(status_code=400, detail="Username is taken")
    hashed_pass = auth_handler.get_password_hash(user_auth.password)

    # replace plaintext pass with hashed pass
    user = User(username=user_auth.username, password=hashed_pass)
    await user.create()

    return user
