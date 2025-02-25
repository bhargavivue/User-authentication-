from pydantic import BaseModel,EmailStr 


class UserProfile(BaseModel):
    username: str
    email: EmailStr
    password:str
class UserResponsemodel(BaseModel): 
    username:str
    email:str
