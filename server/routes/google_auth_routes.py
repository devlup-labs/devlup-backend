from fastapi import APIRouter, Depends
from server.auth import get_current_user
from server.schemas.user_schema import GoogleAuthRequest, GoogleAuthResponse, UserResponse
from server.controllers.google_auth_controller import (
    google_auth_controller,
    get_user_profile_controller,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/google", response_model=GoogleAuthResponse)
async def google_sign_in(auth_request: GoogleAuthRequest):
    """
    Authenticate with Google Sign-In.

    The client sends the Google ID token obtained from the Google Sign-In SDK.
    The server verifies it, creates or updates the user, and returns a JWT.
    """
    return await google_auth_controller(auth_request)


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(current_user: dict = Depends(get_current_user)):
    """
    Get the profile of the currently authenticated user.
    Requires a valid JWT in the Authorization header.
    """
    return await get_user_profile_controller(current_user["sub"])
