from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.user import User
from models.follower import Follower

# --------------------------------------------------------
# FOLLOW A USER
# --------------------------------------------------------
def follow_user_service(db: Session, current_user: User, username: str):
    # Cannot follow yourself
    if username == current_user.username:
        raise HTTPException(status_code=400, detail="You cannot follow yourself")

    # Target user
    target_user = db.query(User).filter(User.username == username).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check already following
    existing = db.query(Follow).filter(
        Follower.follower_id == current_user.id,
        Follower.following_id == target_user.id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Already following this user")

    # Create follow
    follow = Follow(
        follower_id=current_user.id,
        following_id=target_user.id
    )

    db.add(follow)
    db.commit()
    db.refresh(follow)
    return follow

# --------------------------------------------------------
# UNFOLLOW A USER
# --------------------------------------------------------
def unfollow_user_service(db: Session, current_user: User, username: str):
    target_user = db.query(User).filter(User.username == username).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    follow = db.query(Follow).filter(
        Follow.follower_id == current_user.id,
        Follow.following_id == target_user.id
    ).first()

    if not follow:
        raise HTTPException(status_code=400, detail="You are not following this user")

    db.delete(follow)
    db.commit()
    return {"message": f"Unfollowed {username}"}

# --------------------------------------------------------
# GET FOLLOWERS OF A USER
# --------------------------------------------------------
def get_followers_service(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Followers => people who follow THIS user
    followers = (
        db.query(Follower)
        .filter(Follower.following_id == user.id)
        .all()
    )
    return followers

# --------------------------------------------------------
# GET USERS FOLLOWED BY A USER
# --------------------------------------------------------
def get_following_service(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Following => people THIS user follows
    following = (
        db.query(Follower)
        .filter(Follower.follower_id == user.id)
        .all()
    )
    return following