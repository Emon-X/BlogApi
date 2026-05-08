from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Generator
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


if not DATABASE_URL:
    raise ValueError("DATABASE_URL not in .env file")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)
Base = declarative_base()

sessionLocal = sessionmaker(autocommit=False,autoflush=True,bind=engine)

def get_db()->Generator:
    db = sessionLocal()
    
    try:
        yield db
    finally:
        db.close()


