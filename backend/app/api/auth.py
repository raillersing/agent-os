"""
Authentication API Routes
"""

import secrets

from fastapi import APIRouter, HTTPException, status

from ..config import settings
from ..core.security import create_access_token
from ..schemas.auth import TokenRequest, TokenResponse

router = APIRouter()


@router.post("/token", response_model=TokenResponse)
async def create_token(request: TokenRequest):
    """Create a token for the environment-configured bootstrap administrator."""
    if not settings.ADMIN_EMAIL or not settings.ADMIN_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication is not configured",
        )
    if request.email != settings.ADMIN_EMAIL or not secrets.compare_digest(
        request.password, settings.ADMIN_PASSWORD
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        data={"sub": request.email, "email": request.email}
    )
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=3600,
    )
