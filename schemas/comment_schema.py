# schemas/comment.py
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from schemas.user_schema import UserOut  # assuming you have UserOut schema

# Schema for creating a comment
class CommentCreate(BaseModel):
    content: str

# Schema for updating a comment
class CommentUpdate(BaseModel):
    content: str

# Schema for returning comment in response
class CommentOut(BaseModel):
    id: UUID
    post_id: UUID
    user: UserOut   # nested user info
    content: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
