import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

# --------------------------------------------------------
# LOAD DATABASE URL FROM ENVIRONMENT VARIABLES
# --------------------------------------------------------
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL is not set in environment variables")

# --------------------------------------------------------
# INITIALIZE DATABASE ENGINE
# --------------------------------------------------------
engine = create_engine(DATABASE_URL)

# --------------------------------------------------------
# CREATE SESSION FACTORY FOR DB CONNECTIONS
# --------------------------------------------------------
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --------------------------------------------------------
# BASE CLASS FOR ALL SQLALCHEMY MODELS
# --------------------------------------------------------
Base = declarative_base()

# --------------------------------------------------------
# PROVIDE A DATABASE SESSION FOR EACH REQUEST
# --------------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --------------------------------------------------------
# CREATE ALL DATABASE TABLES (IF NOT ALREADY PRESENT)
# --------------------------------------------------------
def create_tables():

    from models import User, Follower, Post, Comment

    print("Creating tables (if they don't exist)...")
    Base.metadata.create_all(bind=engine)
    print("Tables are ready!")
