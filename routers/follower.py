from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from routers.auth import get_current_user
from schemas.follower_schema import FollowerOut
from services.follower_service import follow_user_service, unfollow_user_service, get_followers_service, get_following_service

router = APIRouter()

# ---------------------------------------------------
# GET Followers => people who follow THIS user
# ---------------------------------------------------
@router.get("/{username}/followers", response_model=list[FollowerOut])
def get_followers(
    username: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return get_followers_service(db, username)

# ---------------------------------------------------
# GET Following => people THIS user follows
# ---------------------------------------------------
@router.get("/{username}/following", response_model=list[FollowerOut])
def get_following(
    username: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return get_following_service(db, username)

# -------------------------------------
# POST /api/v1/users/{username}/follow
# -------------------------------------
@router.post("/{username}/follow", response_model=FollowerOut)
def follow_user(
    username: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return follow_user_service(db, current_user, username)

# ----------------------------------------
# DELETE /api/v1/users/{username}/follow
# ----------------------------------------
@router.delete("/{username}/follow")
def unfollow_user(
    username: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return unfollow_user_service(db, current_user, username)

