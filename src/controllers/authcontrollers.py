from fastapi import HTTPException, status, Response, Depends
from src.db.db import user_collection, session_collection
from src.utils.sessionConfig import hash_password, verify_password, create_session
from src.models.models import UserCreate
from bson import ObjectId
from fastapi.responses import JSONResponse
from fastapi import Request

# Controller for creating a user
def create_user(user: UserCreate, response: Response):
    # Check if the email is already registered
    if user_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    # Hash the password before storing
    hashed_password = hash_password(user.password)
    
    user_data = {
        "username": user.username,
        "email": user.email,
        "password": hashed_password,
        # "created_at": datetime.utcnow()  # Uncomment this if you need the 'created_at' field
    }

    # Insert the user data into MongoDB
    result = user_collection.insert_one(user_data)
    
    # Generate session token and store it in the session collection
    session_data = create_session(str(result.inserted_id))
    session_collection.insert_one(session_data)

    # Set the session token in cookies
    response.set_cookie(
        key="session_token",
        value=session_data["session_token"],
        httponly=True,
        secure=False,  # Set this to True when using HTTPS in production
        max_age=3600  # Optional: Set an expiration time for the session token cookie (1 hour in this case)
    )

    # Return a success message along with the user ID
    return {"message": "User created successfully", "user_id": str(result.inserted_id)}

# Controller for user login
def user_login(data):
    # Find the user by email
    user = user_collection.find_one({"email": data.email})  # Use dot notation
    if not user or not verify_password(data.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # Generate session token and store it in the session collection
    session_data = create_session(str(user["_id"]))
    session_collection.insert_one(session_data)

    # Prepare response
    response = Response(content="Login successful")
    response.set_cookie(
        key="session_token",
        value=session_data["session_token"],
        httponly=True,
        secure=False,  # Set to True in production
        max_age=3600  # Expiration time: 1 hour
    )
    return response

# Controller for checking session validity and retrieving user info
def get_user_by_session(request: Request):
    # Retrieve session token from cookies
    session_token = request.cookies.get("session_token")
    if not session_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session token is missing")

    # Check if the session token exists in the session collection
    session = session_collection.find_one({"session_token": session_token})
    if not session:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session")

    # Retrieve user information associated with the session
    user = user_collection.find_one({"_id": ObjectId(session["user_id"])})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Return user information excluding the password
    return {
        "username": user["username"],
        "email": user["email"]
    }
