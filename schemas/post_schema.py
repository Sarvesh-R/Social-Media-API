from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from schemas.user_schema import UserOut
from schemas.comment_schema import CommentOut  # for nested comments

# ---------------------------
# Schema for creating a post
# ---------------------------
class PostCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=2000)
    image_url: Optional[str] = None

# ---------------------------
# Schema for updating a post
# ---------------------------
class PostUpdate(BaseModel):
    content: Optional[str] = Field(None, min_length=1, max_length=2000)
    image_url: Optional[str] = None

# ---------------------------
# Schema for output / response
# ---------------------------
class PostOut(BaseModel):
    id: UUID
    user: UserOut  # nested user info
    content: str
    image_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    comments: List[CommentOut] = []  # optional, can include comments

    class Config:
        orm_mode = True
