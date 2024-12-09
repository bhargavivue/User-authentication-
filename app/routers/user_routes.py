from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.databse import get_db
from app.schemas.user_schemas import UserProfile
from app.services.user_service import get_user_profile, change_password
from app.core.auth import decode_token

router = APIRouter()

# Get User Profile (Authenticated)
@router.get("/profile", response_model=UserProfile)
def get_profile(db: Session = Depends(get_db), token: str = Depends(decode_token)):
    if token is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    print("user:"+token["sub"])
    user = get_user_profile(db, token["sub"])
    return UserProfile(username=user.username,email=user.email,password=user.password)

# Change Password (Authenticated)
@router.post("/change-password")
def change_password_route(new_password: str, db: Session = Depends(get_db), token: str = Depends(decode_token)):
    if token is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = get_user_profile(db, token["sub"])
    return change_password(db, user.id, new_password)
