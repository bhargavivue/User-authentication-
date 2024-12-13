from pydantic import EmailStr
from app.repositories.user_repository import get_user_by_email, save_password_to_history, get_password_history
from fastapi import HTTPException
from app.core.auth import hash_password, verify_password

# Change Password Service
def change_password(db, user_id: int, new_password: str):
    password_history = get_password_history(db, user_id)
    for entry in password_history:
        if verify_password(new_password, entry.hashed_password):
            raise HTTPException(status_code=400, detail="New password cannot be one of the previous 6 passwords")

    # Hash the new password and save it
    hashed_password = hash_password(new_password)
    save_password_to_history(db, user_id, hashed_password)
    return {"message": "Password changed successfully"}

# Get User Profile Service
def get_user_profile(db, email: EmailStr):
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
def get_user_email_password(email:EmailStr, password:str, db):
    user=get_user_email_password(db,EmailStr)
    return user
    