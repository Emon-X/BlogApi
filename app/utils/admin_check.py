from fastapi import HTTPException
from app.database.schemes.user import User

def admin_check(user_data : User):
    if not user_data.is_admin:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return True