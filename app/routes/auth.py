from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.responses import JSONResponse
from app.database.schemes.user import User
from app.database.schemes.blog import Blog
from app.models.auth import User_Login,User_Register
from app.models.blogs import Create_Post,Comment,Like,Update_Post,Responses,TokenResponse
from app.database.repository.user import UserRepository
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.security.auth import AuthHelper
from app.security.hash import Hash_helper
from app.dependencis import get_current_user


router = APIRouter(
    prefix="/auth",
)

@router.post("/Register",status_code=status.HTTP_201_CREATED,tags=["auth"])
def Register(user_data : User_Register, db : Session = Depends(get_db)):
    
    existing_user = db.query(User).filter((User.username==user_data.username)|(User.email==user_data.email)).first()
    
    if existing_user:
        raise HTTPException(status_code=400,detail="username or email already exists")
    
    new_user = UserRepository(db).create_user(user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    token = AuthHelper.encode(new_user.username, new_user.email)
    
    return {"Bearer Token : ": token}

@router.post("/Login",status_code=status.HTTP_200_OK,tags=["auth"])
def Login(user_data : User_Login, db : Session = Depends(get_db)):
    
    user = db.query(User).filter(User.email==user_data.email).first()
    
    if not user or not Hash_helper.verify_password(user_data.password, user.password):
        raise HTTPException(status_code=401,detail="Invalid email or password")
    
    token = AuthHelper.encode(user.username, user.email)
    return {"Bearer Token : ": token}
    