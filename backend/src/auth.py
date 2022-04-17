import jwt

from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta


class AuthHandler:
    """Handles authentication"""

    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = "SECRET"

    def get_password_hash(self, password):
        """returns hashed password"""
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        """checks if plain password and hashed password match"""
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_token(self, user_id):
        """encodes JWT according to user id"""
        payload = {
            "exp": datetime.utcnow() + timedelta(days=0, hours=2),
            "iat": datetime.utcnow(),
            "sub": user_id,
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    def decode_token(self, token):
        """
        decodes JWT and returns token subject if valid
        returns 401 http exception if invalid or expired token
        """
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=401, detail="Expired token. Please renew the token"
            )
        except jwt.InvalidAlgorithmError:
            raise HTTPException(status_code=401, detail="Invalid token")

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        """
        dependency injection wrapper
        checks if http bearer exists through dependency injection, then decodes token if it exists
        """
        return self.decode_token(auth.credentials)
