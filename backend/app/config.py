from decouple import config
from pydantic import BaseModel


class Settings(BaseModel):
    """Server config settings"""

    # Mongo Engine settings
    mongo_uri = config("MONGO_URI")

    # Security settings
    authjwt_secret_key = config("SECRET_KEY")

    testing = config("TESTING", default=False, cast=bool)


CONFIG = Settings()
