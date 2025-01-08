from fastapi import FastAPI
from src.routes.authroutes import router as auth_router

app = FastAPI()

# Ensure this line is present to include the routes
app.include_router(auth_router, prefix="/auth", tags=["auth"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
