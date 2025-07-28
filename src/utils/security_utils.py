from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from config import settings
import secrets

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_value(value: str) -> str:
    return pwd_context.hash(value)

def verify_hash(plain_value: str, hashed_value: str) -> bool:
    return pwd_context.verify(plain_value, hashed_value)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def create_refresh_token():
    refresh_token = secrets.token_hex(32)
    refresh_token_hash = pwd_context.hash(refresh_token)
    return refresh_token, refresh_token_hash
