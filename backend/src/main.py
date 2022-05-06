from src.app import app
from src.api.users import router as users_router
from src.api.posts import router as posts_router


app.include_router(users_router)
app.include_router(posts_router)
