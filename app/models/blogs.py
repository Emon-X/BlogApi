from pydantic import BaseModel, Field
from typing import Optional


class Create_Post(BaseModel):
    
    title : str = Field(...,max_length=100,description="title of the Blog")
    description : str = Field(...,description="details about the blog")
    
    
class Update_Post(BaseModel):
    
    title : Optional[str]
    description : Optional[str]
    
class Responses(BaseModel):
    
    user_name : str
    user_email : str
    title : str
    description : str

class TokenResponse(BaseModel):
    
    access_token : str = Field(..., description="JWT access token")
    token_type : str = "bearer"

class Like(BaseModel):
    
    like : bool = False
    
class Comment(BaseModel):
    
    content : Optional[str] = Field(None, alias="comment")
    
    class Config:
        populate_by_name = True