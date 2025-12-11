from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from db import get_db
from models.post import Post
from schemas.post_schema import PostCreate, PostUpdate, PostOut
from services.post_service import (
    create_post, get_all_posts, get_post_by_id,
    update_post, delete_post
)
from routers.auth import get_current_user

router = APIRouter()

# ------------------------------------------
# CREATE POST (AUTH REQUIRED)
# ------------------------------------------
@router.post("", response_model=PostOut)
def create_new_post(
    post_data: PostCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return create_post(db, current_user.id, post_data)

# ------------------------------------------
# LIST POSTS (PUBLIC FEED)
# ------------------------------------------
@router.get("", response_model=list[PostOut])
def list_posts(db: Session = Depends(get_db)):
    return get_all_posts(db)

# ------------------------------------------
# GET SINGLE POST WITH COMMENTS
# ------------------------------------------
@router.get("/{post_id}", response_model=PostOut)
def get_single_post(post_id: UUID, db: Session = Depends(get_db)):
    post = get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

# ------------------------------------------
# UPDATE OWN POST
# ------------------------------------------
@router.patch("/{post_id}", response_model=PostOut)
def edit_post(
    post_id: UUID,
    update_data: PostUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return update_post(db, post_id, current_user.id, update_data)

# ------------------------------------------
# DELETE OWN POST
# ------------------------------------------
@router.delete("/{post_id}")
def remove_post(
    post_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    delete_post(db, post_id, current_user.id)
    return {"message": "Post deleted successfully"}
