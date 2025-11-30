"""
FastAPI dependencies are very powerful but sometimes a little confusing.

Worth reading up on via https://fastapi.tiangolo.com/tutorial/dependencies/.
"""

from typing import Annotated

import jwt
from fastapi import HTTPException, Request
from fastapi.params import Header
from fastapi_throttle import RateLimiter

from app.auth import get_azure_devops_settings


async def validate_authorization_header(authorization: Annotated[str, Header()]) -> str:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization bearer token required")
    try:
        secret_key = get_azure_devops_settings().JWT_SECRET_STRING
        token = authorization.removeprefix("Bearer ").strip()
        _ = jwt.decode(token, secret_key, algorithms=["HS256"])  # Don't need to return it, just need to know it's valid
        return authorization
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def _extract_auth_header(request: Request) -> str:
    auth = request.headers.get("Authorization")
    if auth:
        return auth.removeprefix("Bearer ").strip()
    else:
        return "unknown"


limiter = RateLimiter(times=5, seconds=60, key_func=_extract_auth_header, add_headers=True)
