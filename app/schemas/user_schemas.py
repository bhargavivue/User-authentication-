from pydantic import BaseModel,EmailStr, Field


class UserProfile(BaseModel):
    username: str
    email: EmailStr
    password: str 