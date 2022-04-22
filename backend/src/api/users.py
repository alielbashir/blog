from fastapi import APIRouter, HTTPException
from src.auth import AuthHandler

from src.models.user import User, UserAuth, UserOut, UserRegister

auth_handler = AuthHandler()

router = APIRouter(prefix="/users")


@router.post("/register", status_code=201, response_model=UserOut)
async def register(user_register: UserRegister):
    user = await User.find_one(User.username == user_register.username)
    if user is not None:
        raise HTTPException(status_code=400, detail="Username is taken")
    hashed_pass = auth_handler.get_password_hash(user_register.password)

    # replace plaintext pass with hashed pass
    user = User(
        username=user_register.username, password=hashed_pass, scope=user_register.scope
    )
    await user.create()

    return user


@router.post("/login")
async def login(user_auth: UserAuth):
    user = await User.find_one(User.username == user_auth.username)

    if user is None or not auth_handler.verify_password(
        user_auth.password, user.password
    ):
        raise HTTPException(status_code=401, detail="Invalid username and/or password")
    token = auth_handler.encode_token(user.username)

    return {"token": token}
