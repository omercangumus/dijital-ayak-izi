import base64
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Any

from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

from ..core.config import settings


def hash_email_for_storage(email: str) -> str:
    # One-way hash + salt (secret_key)
    salted = f"{email.lower()}::{settings.secret_key}".encode("utf-8")
    return hashlib.sha256(salted).hexdigest()


def get_timed_serializer() -> URLSafeTimedSerializer:
    return URLSafeTimedSerializer(secret_key=settings.secret_key, salt="email-verify")


def generate_email_verify_token(email: str) -> str:
    s = get_timed_serializer()
    return s.dumps({"email": email.lower()})


def verify_email_token(token: str, max_age_seconds: int) -> str | None:
    s = get_timed_serializer()
    try:
        data = s.loads(token, max_age=max_age_seconds)
        return data.get("email")
    except (BadSignature, SignatureExpired):
        return None


