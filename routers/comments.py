from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from db import get_db
from services.comment_service import (
    create_comment,
    list_comments_for_post,
    update_comment,
    delete_comment
)
from schemas.comment_schema import CommentCreate, CommentUpdate, CommentOut
from routers.auth import get_current_user

router = APIRouter()

# --------------------------------------------------------
# ADD COMMENT TO A POST
# --------------------------------------------------------
@router.post("/posts/{post_id}/comments", response_model=CommentOut)
def add_comment(
    post_id: UUID,
    data: CommentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return create_comment(db, post_id, current_user.id, data)

# --------------------------------------------------------
# LIST COMMENTS OF A POST (PUBLIC)
# --------------------------------------------------------
@router.get("/posts/{post_id}/comments", response_model=list[CommentOut])
def get_comments(post_id: UUID, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return list_comments_for_post(db, post_id)

# --------------------------------------------------------
# UPDATE COMMENT (ONLY OWNER)
# --------------------------------------------------------
@router.patch("/comments/{comment_id}", response_model=CommentOut)
def edit_comment(
    comment_id: UUID,
    data: CommentUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return update_comment(db, comment_id, current_user.id, data)

# --------------------------------------------------------
# DELETE COMMENT (ONLY OWNER)
# --------------------------------------------------------
@router.delete("/comments/{comment_id}")
def remove_comment(
    comment_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    delete_comment(db, comment_id, current_user.id)
    return {"message": "Comment deleted successfully"}
