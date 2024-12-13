from fastapi import FastAPI
from app.routers import auth_routes, user_routes
from app.databse import engine, Base

app = FastAPI()

# Include routers for authentication and user-related routes
app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
app.include_router(user_routes.router, prefix="/users", tags=["users"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI project!"}

@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)
