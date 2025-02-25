from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.databse import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    # Relationship to password history (one-to-many)
    password_history = relationship("PasswordHistory", back_populates="user")
# Relationship to password history (one-to-many)
    password_history = relationship(
        "PasswordHistory", 
        back_populates="user", 
        cascade="all, delete"
    )