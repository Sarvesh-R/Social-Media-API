# services/user_service.py
from sqlalchemy.orm import Session
from models.user import User
from schemas.user_schema import UserCreate, UserUpdate
from utils.hashing import hash_password, verify_password
from fastapi import HTTPException, status

# ----------------------------------------------------------
# CREATE USER
# ----------------------------------------------------------
def create_user(db: Session, user: UserCreate):
    """Create a new user with hashed password"""
    hashed_password = hash_password(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password,
        full_name=user.full_name,
        bio=user.bio,
        profile_image=user.profile_image
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# ----------------------------------------------------------
# AUTHENTICATE USER
# ----------------------------------------------------------
def authenticate_user(db: Session, username: str = None, email: str = None, password: str = None):
    """
    Authenticate a user by username or email and password.
    Returns the User instance if valid, else raises HTTPException.
    """
    if not (username or email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either username or email must be provided"
        )

    # Fetch user
    user = None
    if username:
        user = db.query(User).filter(User.username == username).first()
    elif email:
        user = db.query(User).filter(User.email == email).first()

    # Validate password
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    return user

# --------------------------------------------------------
# GET PUBLIC PROFILE OF A USER
# --------------------------------------------------------
def get_public_profile_service(db: Session, username: str):
    """Return a public user profile using username"""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

# --------------------------------------------------------
# UPDATE AUTHENTICATED USER'S OWN PROFILE
# --------------------------------------------------------
def update_own_profile_service(db: Session, current_user: User, update_data: UserUpdate):
    """Update profile of logged-in user"""

    if update_data.full_name is not None:
        current_user.full_name = update_data.full_name

    if update_data.bio is not None:
        current_user.bio = update_data.bio

    if update_data.profile_image is not None:
        current_user.profile_image = update_data.profile_image

    db.commit()
    db.refresh(current_user)
    return current_user