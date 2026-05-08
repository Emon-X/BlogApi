from app.database.db import Base
from sqlalchemy import Integer, String, Column, Boolean,DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship


class User(Base):
    
    __tablename__="users"
    id = Column(Integer,primary_key=True,index=True)
    username = Column(String,unique=True,index=True,nullable=False)
    email = Column(String,unique=True,index = True,nullable=False)
    password = Column(String,nullable=False)
    is_active = Column(Boolean,default=True)
    is_admin = Column(Boolean,default=False)
    created_at = Column(DateTime,default=datetime.utcnow)
    
    blogs = relationship("Blog", back_populates="user", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")

    class Config:
        orm_mode = True
    
class Comment(Base):
    
    __tablename__="comments"
    id = Column(Integer,primary_key=True,index=True)
    content = Column(String,nullable=False)
    username = Column(String,nullable=True)
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    blog_id = Column(Integer,ForeignKey("blogs.id",ondelete="CASCADE"),nullable=False)
    created_at = Column(DateTime,default=datetime.utcnow)
    
    user = relationship("User", back_populates="comments")
    blog = relationship("Blog", back_populates="comments")
    
    class Config:
        orm_mode = True