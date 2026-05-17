from fastapi import HTTPException
from datetime import datetime
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from server.core.database import user_collection
from server.projects_website.auth import create_access_token
from server.projects_website.schemas.user_schema import GoogleAuthRequest
import os

GOOGLE_CLIENT_ID = os.getenv("PROJECTS_GOOGLE_CLIENT_ID")


async def google_auth_controller(auth_request: GoogleAuthRequest):
    """
    Verify Google ID token, upsert user in the database,
    and return a JWT access token with the user profile.
    """
    try:
        # Verify the Google ID token against Google's public keys
        idinfo = id_token.verify_oauth2_token(
            auth_request.token,
            google_requests.Request(),
            GOOGLE_CLIENT_ID,
        )
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Invalid Google token",
        )

    # Extract user info from the verified token
    google_id = idinfo["sub"]
    email = idinfo.get("email")
    name = idinfo.get("name")
    picture = idinfo.get("picture")

    if not email:
        raise HTTPException(
            status_code=400,
            detail="Email not available from Google account",
        )

    # Check if user already exists
    existing_user = await user_collection.find_one({"google_id": google_id})

    now = datetime.utcnow()

    if existing_user:
        # Update last login and refresh profile info
        await user_collection.update_one(
            {"google_id": google_id},
            {
                "$set": {
                    "name": name,
                    "picture": picture,
                    "last_login": now,
                }
            },
        )
        user = await user_collection.find_one({"google_id": google_id})
    else:
        # Create new user
        new_user = {
            "email": email,
            "name": name,
            "picture": picture,
            "google_id": google_id,
            "role": "user",
            "created_at": now,
            "last_login": now,
        }
        result = await user_collection.insert_one(new_user)
        user = await user_collection.find_one({"_id": result.inserted_id})

    # Build response
    user_id = str(user["_id"])
    user_response = {
        "id": user_id,
        "email": user["email"],
        "name": user.get("name"),
        "picture": user.get("picture"),
        "role": user["role"],
        "created_at": user.get("created_at"),
        "last_login": user.get("last_login"),
    }

    # Create JWT with user info
    access_token = create_access_token(
        data={
            "sub": user_id,
            "email": email,
            "role": user["role"],
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_response,
    }


async def get_user_profile_controller(user_id: str):
    """Fetch a user's profile by their database ID."""
    from bson import ObjectId

    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")

    user = await user_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user["id"] = str(user["_id"])
    del user["_id"]
    return user
