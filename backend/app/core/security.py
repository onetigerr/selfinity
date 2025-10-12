"""Password hashing and JWT helpers."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict
import warnings

from jose import JWTError, jwt

# Suppress deprecation warning emitted by passlib importing stdlib 'crypt'
warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning,
    module=r"passlib\.utils",
    message=r".*'crypt' is deprecated.*",
)

from passlib.context import CryptContext

from .config import get_settings

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Return a secure hash for the given password."""
    return _pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    """Verify a plaintext password against a hash."""
    return _pwd_context.verify(password, hashed)


def create_access_token(data: Dict[str, Any]) -> str:
    """Create a signed JWT with an expiry from settings."""
    settings = get_settings()
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=settings.access_token_expires_days)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return token


def decode_access_token(token: str) -> Dict[str, Any]:
    """Decode and validate a JWT, returning its payload or raising JWTError.

    To avoid a DeprecationWarning from python-jose (uses utcnow internally), we
    disable built-in exp verification and validate expiration ourselves using
    timezone-aware datetimes.
    """
    settings = get_settings()
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
            options={"verify_exp": False},
        )
    except JWTError as exc:
        raise exc

    # Manual expiration check
    exp = payload.get("exp")
    if exp is None:
        # Treat missing exp as invalid token
        raise JWTError("Token missing exp claim")

    now_ts = datetime.now(timezone.utc).timestamp()
    try:
        exp_ts = float(exp)  # jose returns NumericDate as int/float
    except (TypeError, ValueError):
        # If jose returned a non-numeric, attempt to parse datetime-like
        if hasattr(exp, "timestamp"):
            exp_ts = float(exp.timestamp())  # type: ignore[call-arg]
        else:
            raise JWTError("Invalid exp claim type")

    if now_ts >= exp_ts:
        raise JWTError("Token has expired")

    return payload
