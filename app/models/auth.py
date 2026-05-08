from pydantic import BaseModel,EmailStr, field_validator, Field
from typing import Optional

class User_Register(BaseModel):
    
    username : str = Field(...,min_length=3,max_length=10,examples=["Emon"])
    email: EmailStr = Field(...,examples=["Emon@gmail.com"])
    password : str = Field(...,min_length=6,examples=["password"])
    confirm_password : str = Field(...,min_length=6,examples=["confirm password"])
    
    @field_validator('confirm_password')
    @classmethod
    def password_match(cls,value,values):
        
        if 'password' in values.data and value!=values.data['password']:
            raise ValueError("Password not match")
        
        return value
    
class User_Login(BaseModel):
    
    email : EmailStr = Field(...,examples=["Emon@gmail.com"])
    password : str = Field(...,min_length=6,examples=["password"])