from app.database.schemes.user import User
from app.database.repository.user import UserRepository
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.utils.protected_routes import get_current_user
from app.utils.admin_check import admin_check
from fastapi import APIRouter, Depends, HTTPException, status
from dotenv import load_dotenv
from app.security.hash import Hash_helper
from app.security.auth import AuthHelper
import os
load_dotenv()

admin_username = os.getenv("ADMIN_USERNAME")
admin_email = os.getenv("ADMIN_EMAIL")
admin_password = os.getenv("ADMIN_PASSWORD")


def create_admin():
    db = None
    try:
        if not admin_username or not admin_email or not admin_password:
            print("Admin credentials not configured in environment variables")
            return
        
        db = next(get_db())
        admin_user = UserRepository(db).get_user_by_email(admin_email)
        if not admin_user:
            new_admin = User(
                username=admin_username,
                email=admin_email,
                password=Hash_helper.get_password_hash(admin_password),
                is_admin=True
            )
            db.add(new_admin)
            db.commit()
            db.refresh(new_admin)
            
            token = AuthHelper.encode(username=admin_username, email=admin_email)
            print(f"Admin user created successfully. Token: {token}")
        else:
            print("Admin user already exists")
    except Exception as e:
        print(f"Error creating admin user: {str(e)}")
    finally:
        if db:
            db.close()