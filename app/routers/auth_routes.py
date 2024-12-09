from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.databse import get_db
from app.repositories.user_repository import get_user_by_email, create_user, save_password_to_history
from app.core.auth import create_access_token, hash_password, verify_password 
from app.schemas.auth_schemas import Token, UserCreateRequest, UserLoginRequest
from app.utils.email_utils import send_email

router = APIRouter()

# User Registration
@router.post("/register")
def register(user: UserCreateRequest, db: Session = Depends(get_db)):
    # Check if the email is already registered
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password
    hashed_password = hash_password(user.password)
    
    # Create user
    user = create_user(db, user.username, user.email, hashed_password)

    # Save password history
    save_password_to_history(db, user.id, hashed_password)
    
    # Send confirmation email
    #send_email(user.email, "Welcome to Our Service", "Thank you for registering with us!")
    
    return {"message": "User registered successfully"}

# Login route for generating JWT token
@router.post("/login", response_model=Token)
def login(user: UserLoginRequest, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
