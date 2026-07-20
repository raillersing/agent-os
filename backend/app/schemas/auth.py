"""
Authentication Schemas
"""

from pydantic import BaseModel


class TokenRequest(BaseModel):
    """Token request schema."""

    email: str
    password: str


class TokenResponse(BaseModel):
    """Token response schema."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int = 3600
