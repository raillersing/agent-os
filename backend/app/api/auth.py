"""
Authentication API Routes
"""

import secrets
from datetime import timedelta

from fastapi import APIRouter, HTTPException, Response, status

from ..config import settings
from ..core.security import create_access_token
from ..schemas.auth import TokenRequest, TokenResponse

router = APIRouter()


@router.post("/token", response_model=TokenResponse)
async def create_token(response: Response, request: TokenRequest):
    """Create a token for the environment-configured bootstrap administrator.

    The token is also returned as an httpOnly cookie for browser clients.
    """
    if not settings.ADMIN_EMAIL or not settings.ADMIN_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication is not configured",
        )
    if request.email != settings.ADMIN_EMAIL or not secrets.compare_digest(
        request.password, settings.ADMIN_PASSWORD
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    expires_in = 3600
    access_token = create_access_token(
        data={"sub": request.email, "email": request.email},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=expires_in,
        path="/",
    )
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=expires_in,
    )


@router.post("/logout")
async def logout(response: Response):
    """Clear the browser authentication cookie."""
    response.delete_cookie(key="access_token", path="/")
    return {"detail": "Logged out"}
