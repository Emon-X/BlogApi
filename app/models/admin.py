from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class Comment_Response(BaseModel):
    id: int
    content: str
    username: Optional[str]
    user_id: int
    blog_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class User_Response(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    is_admin: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class User_Update(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None


class Blog_Response(BaseModel):
    id: int
    title: str
    description: str
    username: str
    user_id: int
    created_at: datetime
    updated_at: datetime
    comments: Optional[list[Comment_Response]] = None
    
    class Config:
        from_attributes = True


class Blog_Update(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
        