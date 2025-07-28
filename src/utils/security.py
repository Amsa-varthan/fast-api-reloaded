# security.py
import secrets
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import JWTError, jwt
from config import settings

# Hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_value(value: str) -> str:
    return pwd_context.hash(value)

def verify_hash(plain_value: str, hashed_value: str) -> bool:
    return pwd_context.verify(plain_value, hashed_value)

# OTP Generation
def generate_otp(length: int = 6) -> str:
    return "".join([str(secrets.randbelow(10)) for _ in range(length)])

# JWT Access Token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# JWT Refresh Token
def create_refresh_token():
    # Create a sufficiently random string for the refresh token
    refresh_token = secrets.token_urlsafe(32)
    # Return the plain token and its hash
    return refresh_token, hash_value(refresh_token)
