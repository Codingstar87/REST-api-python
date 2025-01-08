from fastapi import APIRouter, Response, Request
from src.controllers.authcontrollers import create_user, user_login, get_user_by_session
from src.models.models import UserCreate, UserLogin

router = APIRouter()

# Register user
@router.post("/register")
async def register_user(user: UserCreate, response: Response):
    return create_user(user, response)

# User login
@router.post("/login")
async def login_user(data: UserLogin):
    return user_login(data)

# Get user info from session token
@router.get("/user")
async def get_user_info(request: Request):
    return get_user_by_session(request)
