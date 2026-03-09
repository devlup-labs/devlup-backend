from fastapi import APIRouter
from schemas.user_schemas import User
from database.db import users
router = APIRouter()
@router.post("/users")
def create_user(user: User):
    users.append(user)
    return {"message": "User created", "user": user}
@router.get("/users")
def get_users():
    return users