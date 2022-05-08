from src.api.posts import router as posts_router
from src.api.users import router as users_router
from src.app import app

app.include_router(users_router)
app.include_router(posts_router)
