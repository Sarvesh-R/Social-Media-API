# schemas/user.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from uuid import UUID
from datetime import datetime

# --------------------------------------------------------
# BASE USER FIELDS (shared by multiple schemas)
# --------------------------------------------------------
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    bio: Optional[str] = None
    profile_image: Optional[str] = None

# --------------------------------------------------------
# SCHEMA FOR USER REGISTRATION
# --------------------------------------------------------
class UserCreate(UserBase):
    password: str 

# --------------------------------------------------------
# SCHEMA FOR UPDATING USER PROFILE (SELF)
# --------------------------------------------------------
class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    bio: Optional[str] = None
    profile_image: Optional[str] = None

# --------------------------------------------------------
# SCHEMA FOR USER DATA SENT IN RESPONSES
# --------------------------------------------------------
class UserOut(UserBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True

# --------------------------------------------------------
# SCHEMA FOR USER LOGIN (USERNAME or EMAIL + PASSWORD)
# --------------------------------------------------------
class UserLogin(BaseModel):
    username: Optional[str] = Field(None, description="Username of the user")
    email: Optional[EmailStr] = Field(None, description="Email of the user")
    password: str = Field(..., description="Password of the user")

    # Validate that at least username or email is provided
    def validate_login(self):
        if not (self.username or self.email):
            raise ValueError("Either username or email must be provided")