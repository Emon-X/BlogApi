from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.responses import JSONResponse
from app.database.schemes.user import User, Comment
from app.database.schemes.blog import Blog
from app.models.auth import User_Login,User_Register
from app.models.blogs import Create_Post,Comment,Like,Update_Post,Responses,TokenResponse
from app.database.repository.user import UserRepository
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.security.auth import AuthHelper
from app.security.hash import Hash_helper
from app.dependencis import get_current_user
from app.database.schemes.user import Comment as CommentModel

router = APIRouter(
    prefix="/blog"
)

@router.post("/Create",status_code=status.HTTP_201_CREATED,tags=["blog"])
def Create(blogs : Create_Post ,current_user : User = Depends(get_current_user), db : Session = Depends(get_db)):
    
    db_blog = Blog(**blogs.model_dump(), user_id=current_user.id, username=current_user.username)
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    
    return db_blog


@router.get("/View",response_model=list[Responses],status_code=status.HTTP_200_OK,tags=["blog"])
def View(current_user : User = Depends(get_current_user), db : Session = Depends(get_db)):
    
    blogs = db.query(Blog).filter(Blog.user_id == current_user.id).all()
    return [
        Responses(
            user_name=blog.username,
            user_email=blog.user.email,
            title=blog.title,
            description=blog.description
        )
        for blog in blogs
    ]

@router.get("/Read/{blog_id}",response_model=Responses,status_code=status.HTTP_200_OK,tags=["blog"])
def Read(blog_id : int,current_user : User = Depends(get_current_user), db : Session = Depends(get_db)):
    
    blog = db.query(Blog).filter(Blog.id==blog_id and Blog.user_id==current_user.id).first()
    
    if not blog:
        raise HTTPException(status_code=404,detail="Blog not found")
    
    return Responses(
        user_name=blog.username,
        user_email=current_user.email,
        title=blog.title,
        description=blog.description
    )


@router.put("/Edit/{blog_id}",status_code=status.HTTP_200_OK,tags=["blog"])
def Edit(blog_id : int, Update_blog : Update_Post ,current_user : User = Depends(get_current_user), db : Session = Depends(get_db)):
    
    blog = db.query(Blog).filter(Blog.id == blog_id and Blog.user_id == current_user.id).first()
    
    if not blog:
        raise HTTPException(status_code=404,detail="Blog not found")
    
    updated_post = Update_blog.model_dump(exclude_unset=True)
    
    for field,value in updated_post.items():
        setattr(blog,field,value)
        
    db.commit()
    db.refresh(blog)
    
    return blog


@router.delete("/Delete/{blog_id}",status_code=status.HTTP_200_OK,tags=["blog"])
def Delete(blog_id : int, current_user : User = Depends(get_current_user), db : Session = Depends(get_db)):
    
    blog = db.query(Blog).filter(Blog.id == blog_id and Blog.user_id == current_user.id).first()
    
    if not blog:
        raise HTTPException(status_code=404,detail="Blog not found")
    
    db.delete(blog)
    db.commit()


@router.post("/Like",tags=["blog"])
def Like(like : Like):
    
    return {"message": "This is the Like page of the Blog!"}


@router.post("/Comment",status_code=status.HTTP_201_CREATED,tags=["blog"])
def Comment(comment_data : Comment, blog_id : int, current_user : User = Depends(get_current_user), db : Session = Depends(get_db)):
    
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    new_comment = CommentModel(
        content=comment_data.content,
        username=current_user.username,
        user_id=current_user.id,
        blog_id=blog_id
    )
    
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    
    return new_comment
    