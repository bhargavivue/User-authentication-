from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from app.databse import get_db
from app.schemas.user_schemas import UserProfile
from app.services.user_service import get_user_profile, change_password
from app.core.auth import decode_token
from app.utils.validation_utils import validate_password

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Define schema for password change request
class ChangePasswordSchema(BaseModel):
    new_password: str

# Get User Profile (Authenticated)
@router.get("/profile", response_model=UserProfile, tags=["users"])
def get_user_profile_api(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    """
    Get the authenticated user's profile.
    """
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token or unauthorized access.")

    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Token payload is invalid.")

    user = get_user_profile(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    return UserProfile(username=user.username, email=user.email)

# Change Password (Authenticated)
@router.post("/change-password", tags=["users"])
def change_password_route(
    password_data: ChangePasswordSchema,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    """
    Change the authenticated user's password.
    """
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token or unauthorized access.")

    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Token payload is invalid.")

    user = get_user_profile(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    validate_password(password_data.new_password)
    change_password(db, user.id, password_data.new_password)

    return {"message": "Password changed successfully"}