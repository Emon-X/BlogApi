from sqlalchemy import Integer,String,Boolean,Column,DateTime, ForeignKey
from app.database.db import Base
from datetime import datetime
from sqlalchemy.orm import relationship


class Blog(Base):
    
    __tablename__="blogs"
    id = Column(Integer,primary_key=True,nullable=False)
    username = Column(String,nullable=False)
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    title = Column(String(100),nullable=False)
    description = Column(String,nullable=False)
    created_at= Column(DateTime,default=datetime.utcnow)
    updated_at = Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="blogs")
    comments = relationship("Comment", back_populates="blog", cascade="all, delete-orphan")
    def __repr__(self):
        return f"<Blog(id ={self.id},username = {self.username},title = {self.title})>"
    
    
