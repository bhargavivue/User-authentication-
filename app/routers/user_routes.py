from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.databse import get_db
from app.schemas.user_schemas import UserProfile
from app.services.user_service import get_user_profile, change_password
from app.core.auth import decode_token
from app.utils.validation_utils import validate_password

router = APIRouter()

# Define the OAuth2 scheme for Swagger documentation
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Get User Profile (Authenticated)
@router.get("/profile", response_model=UserProfile, tags=["users"])
def get_user_profile_api(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),  # Decode the JWT token
):
    """
    Get the authenticated user's profile.
    """
    # Decode and validate the JWT token
    payload = decode_token(authorization=f"Bearer {token}")
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token or unauthorized access.")

    # Extract email from the token payload
    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Token payload is invalid.")

    # Fetch the user profile
    user = get_user_profile(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    # Return the user's profile data
    return UserProfile(
        username=user.username,
        email=user.email,
        password=user.password
        # Avoid including sensitive information like the password
    )

# Change Password (Authenticated)
@router.post("/change-password", tags=["users"])
def change_password_route(
    new_password: str,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),  # Extract Authorization header
):
    """
    Change the authenticated user's password.
    """
    # Decode and validate the JWT token
    payload = decode_token(authorization=f"Bearer {token}")
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token or unauthorized access.")

    # Extract email from the token payload
    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Token payload is invalid.")

    # Fetch the user's current data
    user = get_user_profile(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    # Validate the new password
    validate_password(new_password)

    # Perform the password change
    return change_password(db, user.id, new_password)
