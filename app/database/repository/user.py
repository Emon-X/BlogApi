from app.database.repository.base import BaseRepository
from app.database.schemes.user import User
from app.security.hash import Hash_helper

class UserRepository(BaseRepository):
    
    def create_user(self,user_data: User):
        
        hashed_password = Hash_helper.get_password_hash(user_data.password)
        new_user = User(
            username = user_data.username,
            email = user_data.email,
            password = hashed_password
        )
        
        self.session.add(instance=new_user)
        self.session.commit()
        self.session.refresh(instance=new_user)
        
        return new_user
    
    def get_user_by_email(self,email:str):
        return self.session.query(User).filter(User.email==email).first()
    
    def get_user_by_id(self, user_id: int):
        return self.session.query(User).filter(User.id==user_id).first()
    
    def get_all_users(self):
        return self.session.query(User).all()
        
    