from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from schemas.user_schema import UserOut

# ---------------------------
# Schema for creating a follow
# ---------------------------
class FollowerCreate(BaseModel):
    username: str

# ---------------------------
# Schema for response / output
# ---------------------------
class FollowerOut(BaseModel):
    id: UUID
    follower: UserOut  # the user who is following
    following: UserOut  # the user being followed
    created_at: datetime

    class Config:
        orm_mode = True
