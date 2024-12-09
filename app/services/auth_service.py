from app.core.auth import hash_password, verify_password
from app.repositories.user_repository import get_user_by_email
from fastapi import HTTPException

# Handle login service logic
def authenticate_user(db, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user
