from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import HTTPException
from passlib.context import CryptContext

from config import get_settings

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """
    Service responsible for handling authentication and token-related operations.
    Provides utilities for password hashing, token creation and verification
    using JWT with HS256 algorithm.
    """

    def __init__(self):
        """
        Initializes the AuthService with configuration values such as secret key,
        algorithm, and token expiration time.
        """
        self.secret_key = settings.jwt_secret
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 60

    def verify_password(self, plain_password, hashed_password):
        """
        Verify a plain text password against a hashed password.
        """
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        """
        Hash a plain text password.
        """
        return pwd_context.hash(password)

    def create_access_token(self, data: dict):
        """
        Create a JWT access token containing the provided data.
        The token includes an expiration time based on configured settings.
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def decode_token(self, token: str):
        """
        Decode a JWT token and return its payload.
        """
        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
