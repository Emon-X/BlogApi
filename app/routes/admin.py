from fastapi import APIRouter, Depends, HTTPException, status
from app.database.schemes.user import User
from app.database.schemes.blog import Blog
from app.database.repository.user import UserRepository
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.utils.protected_routes import get_current_user
from app.models.admin import User_Response, Blog_Response, User_Update, Blog_Update, Comment_Response
from app.utils.admin_check import admin_check



router = APIRouter(
    prefix="/admin",
)

@router.get("/users",response_model=list[User_Response],status_code=status.HTTP_200_OK,tags=["admin"])
def get_all_users(current_user : User = Depends(get_current_user), db : Session = Depends(get_db)):
    
    admin_check(current_user)
    
    users = UserRepository(db).get_all_users()
    return users

@router.get("/blogs",response_model=list[Blog_Response],status_code=status.HTTP_200_OK,tags=["admin"])
def get_all_blogs(current_user : User = Depends(get_current_user), db : Session = Depends(get_db)):
    
    admin_check(current_user)
    
    blogs = db.query(Blog).all()
    return blogs


@router.delete("/delete_user/{user_id}",status_code=status.HTTP_204_NO_CONTENT,tags=["admin"])
def delete_user(user_id : int,current_user : User = Depends(get_current_user), db : Session = Depends(get_db)):
    
    admin_check(current_user)
    
    user = UserRepository(db).get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return {"detail": "User deleted successfully"}

@router.delete("/delete_blog/{blog_id}",status_code=status.HTTP_204_NO_CONTENT,tags=["admin"])
def delete_blog(blog_id : int,current_user : User = Depends(get_current_user), db : Session = Depends(get_db)):
    
    admin_check(current_user)
    
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    db.delete(blog)
    db.commit()
    return {"detail": "Blog deleted successfully"}

@router.put("/update_user/{user_id}",response_model=User_Response,status_code=status.HTTP_200_OK,tags=["admin"])
def update_user(user_id : int, updated_user : User_Update ,current_user : User = Depends(get_current_user), db : Session = Depends(get_db)):
    
    admin_check(current_user)
    
    user = UserRepository(db).get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if updated_user.username is not None:
        user.username = updated_user.username
    if updated_user.email is not None:
        user.email = updated_user.email
    if updated_user.is_active is not None:
        user.is_active = updated_user.is_active
    if updated_user.is_admin is not None:
        user.is_admin = updated_user.is_admin
    
    db.commit()
    db.refresh(user)
    
    return user

@router.put("/update_blog/{blog_id}",response_model=Blog_Response,status_code=status.HTTP_200_OK,tags=["admin"])
def update_blog(blog_id : int, updated_blog : Blog_Update ,current_user : User = Depends(get_current_user), db : Session = Depends(get_db)):
    
    admin_check(current_user)

    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    if updated_blog.title is not None:
        blog.title = updated_blog.title
    if updated_blog.description is not None:
        blog.description = updated_blog.description
    
    db.commit()
    db.refresh(blog)
    
    return blog