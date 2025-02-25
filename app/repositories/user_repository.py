from sqlalchemy.orm import Session
from app.models.user import User
from app.models.password_history import PasswordHistory

# Create user
def create_user(db: Session, username: str, email: str, password: str) -> User:
    db_user = User(username=username, email=email, password=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Get user by email
def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()

# Get user by ID
def get_user_by_id(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()

# Save password to history
def save_password_to_history(db: Session, user_id: int, hashed_password: str):
    password_history = PasswordHistory(user_id=user_id, hashed_password=hashed_password)
    db.add(password_history)
    db.commit()
    db.refresh(password_history)

# Get password history for a user
def get_password_history(db: Session, user_id: int):
    return db.query(PasswordHistory).filter(PasswordHistory.user_id == user_id).order_by(PasswordHistory.id.desc()).limit(6).all()

def update_user(db: Session, user_id: int, hashed_password: str):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None  # Handle case where user does not exist
    user.password = hashed_password
    db.commit()
    db.refresh(user)  # Refresh to get the updated user
    return {"message":"user password updated"}
