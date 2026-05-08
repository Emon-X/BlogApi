from fastapi import Depends, HTTPException, status, Header
from app.security.auth import AuthHelper
from app.database.repository.user import UserRepository
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.database.schemes.user import User

def get_current_user(authorization: str = Header(None, alias="Authorization"), db : Session = Depends(get_db))->User:
    
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication scheme")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    
    try:
        payload = AuthHelper.decode(token)
        
        email: str= payload.get("email")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    
    user = db.query(User).filter(User.email==email).first()
    
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"}
        )
        
    return user