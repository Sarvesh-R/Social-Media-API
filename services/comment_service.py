from fastapi import HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime
from models.post import Post
from models.comment import Comment
from schemas.comment_schema import CommentCreate, CommentUpdate

# --------------------------------------------------------
# CREATE COMMENT
# --------------------------------------------------------
def create_comment(db: Session, post_id: UUID, user_id: UUID, data: CommentCreate):

    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    new_comment = Comment(
        post_id=post_id,
        user_id=user_id,
        content=data.content,
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

# --------------------------------------------------------
# LIST COMMENTS FOR A POST
# --------------------------------------------------------
def list_comments_for_post(db: Session, post_id: UUID):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return (
        db.query(Comment)
        .filter(Comment.post_id == post_id)
        .order_by(Comment.created_at.asc())
        .all()
    )

# --------------------------------------------------------
# UPDATE COMMENT (ONLY OWNER)
# --------------------------------------------------------
def update_comment(db: Session, comment_id: UUID, user_id: UUID, data: CommentUpdate):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not allowed to edit this comment")

    comment.content = data.content
    comment.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(comment)
    return comment

# --------------------------------------------------------
# DELETE COMMENT (ONLY OWNER)
# --------------------------------------------------------
def delete_comment(db: Session, comment_id: UUID, user_id: UUID):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not allowed to delete this comment")

    db.delete(comment)
    db.commit()
