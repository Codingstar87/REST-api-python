import hashlib
import os
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from passlib.context import CryptContext
from uuid import uuid4

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Session token generation
def generate_session_token():
    return str(uuid4())

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_session(user_id: str):
    session_token = generate_session_token()
    return {
        "user_id": user_id,
        "session_token": session_token
    }
