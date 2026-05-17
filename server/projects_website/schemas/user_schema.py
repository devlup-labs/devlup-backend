from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class GoogleAuthRequest(BaseModel):
    """Request body for Google Sign-In — expects the ID token from the client."""
    token: str


class GoogleAuthResponse(BaseModel):
    """Response returned after successful Google authentication."""
    access_token: str
    token_type: str = "bearer"
    user: "UserResponse"


class UserResponse(BaseModel):
    """Public user profile returned in auth responses."""
    id: str
    email: str
    name: Optional[str] = None
    picture: Optional[str] = None
    role: str
    created_at: Optional[datetime] = None
    last_login: Optional[datetime] = None


# Rebuild model so the forward reference resolves
GoogleAuthResponse.model_rebuild()
