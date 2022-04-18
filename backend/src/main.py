from src.app import app
from src.api.users import router as usersRouter


app.include_router(usersRouter)
