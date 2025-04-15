from typing import Optional, Dict, Any
from datetime import datetime, timedelta

from passlib.context import CryptContext
from jose import jwt, JWTError, ExpiredSignatureError

from core.config import SecurityConfig


class AuthManager:
    def __init__(self, config: SecurityConfig):
        self.config = config
        self.pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.config.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(claims=to_encode, key=self.config.SECRET_KEY, algorithm=self.config.ALGORITHM)

    def decode_access_token(self, token: str) -> Optional[dict]:
        try:
            payload = jwt.decode(token, self.config.SECRET_KEY, algorithms=[self.config.ALGORITHM])
            return payload
        except (JWTError, ExpiredSignatureError):
            return None
