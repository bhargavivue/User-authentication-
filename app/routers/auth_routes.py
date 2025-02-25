from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.databse import get_db
from app.repositories.user_repository import get_user_by_email, create_user, save_password_to_history
from app.core.auth import create_access_token, hash_password, verify_password 
from app.schemas.auth_schemas import Token, UserCreateRequest, UserLoginRequest
from app.utils.validation_utils import validate_password 

router = APIRouter()

# User Registration
@router.post("/register")
def register(user: UserCreateRequest, db: Session = Depends(get_db)):
    # Validate the password
    validate_password(user.password)
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)
    user = create_user(db, user.username, user.email, hashed_password)
    save_password_to_history(db, user.id, hashed_password)
    
    return {"message": "User registered successfully"}

# Login route for generating JWT token
@router.post("/login", response_model=Token)
def login(userdata: OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    
    db_user = get_user_by_email(db, userdata.username)
    
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not verify_password(userdata.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/get-token", response_model=Token)
def login(userdata:UserLoginRequest,db:Session = Depends(get_db)):
    
    db_user = get_user_by_email(db, userdata.email)
    
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not verify_password(userdata.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": userdata.email})
    return {"access_token": access_token, "token_type": "bearer"}
