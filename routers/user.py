from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from routers.auth import get_current_user
from schemas.user_schema import UserOut, UserUpdate
from services.user_service import (
    get_public_profile_service,
    update_own_profile_service
)

router = APIRouter()

# --------------------------------------------------
# GET /api/v1/users/{username} — Public Profile
# --------------------------------------------------
@router.get("/{username}", response_model=UserOut)
def get_public_profile(username: str, db: Session = Depends(get_db)):
    return get_public_profile_service(db, username)

# --------------------------------------------------
# PATCH /api/v1/users/me — Update Own Profile
# --------------------------------------------------
@router.patch("/me", response_model=UserOut)
def update_my_profile(
    update_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return update_own_profile_service(db, current_user, update_data)


