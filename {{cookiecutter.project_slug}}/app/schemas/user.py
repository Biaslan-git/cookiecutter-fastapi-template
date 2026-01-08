"""
User Pydantic schemas for API validation
"""
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserBase(BaseModel):
    """Base user schema with common fields"""
    email: EmailStr
    username: str = Field(min_length=3, max_length=100)


class UserCreate(UserBase):
    """Schema for creating a user"""
    password: str = Field(min_length=6, max_length=100)


class UserUpdate(BaseModel):
    """Schema for updating a user"""
    email: EmailStr | None = None
    username: str | None = Field(None, min_length=3, max_length=100)
    is_active: bool | None = None


class UserResponse(UserBase):
    """Schema for user response"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
