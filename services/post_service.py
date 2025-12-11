from sqlalchemy.orm import Session
from fastapi import HTTPException
from uuid import UUID
from models.post import Post
from schemas.post_schema import PostCreate, PostUpdate

# ---------------------------------------------------
# CREATE POST
# ---------------------------------------------------
def create_post(db: Session, user_id: UUID, data: PostCreate):
    new_post = Post(
        user_id=user_id,
        content=data.content,
        image_url=data.image_url
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# ---------------------------------------------------
# GET ALL POSTS (PUBLIC FEED)
# ---------------------------------------------------
def get_all_posts(db: Session):
    return (
        db.query(Post)
        .order_by(Post.created_at.desc())
        .all()
    )

# ---------------------------------------------------
# GET SINGLE POST WITH COMMENTS
# ---------------------------------------------------
def get_post_by_id(db: Session, post_id: UUID):
    return db.query(Post).filter(Post.id == post_id).first()

# ---------------------------------------------------
# UPDATE POST
# ---------------------------------------------------
def update_post(db: Session, post_id: UUID, user_id: UUID, data: PostUpdate):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not allowed to edit this post")

    if data.content is not None:
        post.content = data.content

    if data.image_url is not None:
        post.image_url = data.image_url

    db.commit()
    db.refresh(post)
    return post

# ---------------------------------------------------
# DELETE POST
# ---------------------------------------------------
def delete_post(db: Session, post_id: UUID, user_id: UUID):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not allowed to delete this post")

    db.delete(post)
    db.commit()
