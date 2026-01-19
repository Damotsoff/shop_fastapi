from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from core.config import settings


def encode_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
    expire_timedelta: timedelta | None = None,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
) -> str:
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update({"exp": expire, "iat": now})
    encoded = jwt.encode(payload=to_encode, key=private_key, algorithm=algorithm)
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
) -> dict:
    try:
        decoded = jwt.decode(
            token,
            key=public_key,
            algorithms=[algorithm],
        )
    except Exception as e:
        raise e
    return decoded


def hash_password(password: str) -> bytes:
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed


def validate_password(password: str, hashed: bytes) -> bool:
    is_valid = bcrypt.checkpw(password.encode("utf-8"), hashed)
    return is_valid
