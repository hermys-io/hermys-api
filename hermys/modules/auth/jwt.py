from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from jose import jwt

from hermys.settings import get_settings

settings = get_settings()


def create_token(
    *,
    data: Dict[str, Any],
    expires_delta: timedelta | None = None,
):
    data_to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    data_to_encode.update({'exp': expire})

    encoded_jwt = jwt.encode(
        claims=data_to_encode,
        key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    return encoded_jwt
