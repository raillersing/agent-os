"""
Authentication API Routes
"""

from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer

from ..schemas.auth import TokenRequest, TokenResponse
from ..core.security import create_access_token

router = APIRouter()

# In-memory user storage for MVP
users_db = {
    "admin@agent-os.dev": {
        "id": "1",
        "email": "admin@agent-os.dev",
        "password": "admin",  # In production, this would be hashed
        "name": "Admin",
    }
}


@router.post("/token", response_model=TokenResponse)
async def create_token(request: TokenRequest):
    """Create authentication token."""
    user = users_db.get(request.email)
    if not user or user["password"] != request.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user["id"], "email": user["email"]})
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=3600,
    )
