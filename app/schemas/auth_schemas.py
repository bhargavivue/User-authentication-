from pydantic import BaseModel,EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str

class UserCreateRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

