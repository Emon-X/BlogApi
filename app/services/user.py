from sqlalchemy.orm import Session
from app.database.repository.user import UserRepository
from app.database.db import get_db
from app.security.auth import AuthHelper
from app.security.hash import Hash_helper


class UserService:
    
    def __init__(self,session: Session):
        self.user_repository = UserRepository(session.session)
        
    def sign_up(self,user_data):
        
        existing_user = self.user_repository.get_user_by_email(user_data.email)

        if existing_user:
            raise Exception("Email already exists")
        
        new_user = self.user_repository.create_user(user_data)
        
        token = AuthHelper.encode(new_user.username, new_user.email)
        
        return {"Bearer Token: " + token}
    
    def login(self,user_data):
        
        user = self.user_repository.get_user_by_email(user_data.email)
        
        if not user or not Hash_helper.verify_password(user_data.password, user.password):
            raise Exception("Invalid email or password")
        
        token = AuthHelper.encode(user.username, user.email)
        
        return {"Bearer Token: " + token}