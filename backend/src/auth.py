import jwt

from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta

from src.models.user import Scope, User, UserNoPass
from src.config import CONFIG


class AuthHandler:
    """Handles authentication"""

    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = CONFIG.authjwt_secret_key

    def get_password_hash(self, password):
        """returns hashed password"""
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        """checks if plain password and hashed password match"""
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_token(self, user: User) -> str:
        """encodes JWT according to user id and scopes"""
        payload = {
            "exp": datetime.utcnow() + timedelta(days=0, hours=2),
            "iat": datetime.utcnow(),
            "sub": user.username,
            "scope": user.scope,
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    def decode_token(self, token: str) -> UserNoPass:
        """
        decodes JWT and returns a UserNoPass object
        raises 401 http exception if invalid or expired token
        """
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            return UserNoPass(username=payload["sub"], scope=payload["scope"])
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=401, detail="Expired token. Please renew the token"
            )
        except jwt.InvalidAlgorithmError:
            raise HTTPException(status_code=401, detail="Invalid token")

    def authorized(self, auth: HTTPAuthorizationCredentials = Security(security)):
        """
        dependency injection wrapper
        checks if http bearer exists through dependency injection, then decodes token and
        returns a UserNoPass object if a token exists
        """

        return self.decode_token(auth.credentials)

    def write_authorized(self, auth: HTTPAuthorizationCredentials = Security(security)):
        """
        dependency injection wrapper
        authorizes user only if they have write scope
        """
        user = self.decode_token(auth.credentials)
        if user.scope == Scope.write:
            return user
        else:
            raise HTTPException(status_code=403, detail="Unauthorized")
