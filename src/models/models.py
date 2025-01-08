from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str


class SessionCreate(BaseModel):
    user_id: str
    session_token: str

class UserResponse(BaseModel):
    username: str
    email: str

    class Config:
        orm_mode = True
