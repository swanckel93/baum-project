from typing import Optional
from pydantic import EmailStr, Field
from .base import BaseSchema, BaseResponseSchema


class UserBase(BaseSchema):
    """Base user schema with common fields"""
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=255)
    phone: Optional[str] = Field(None, max_length=20)
    is_active: bool = True
    is_admin: bool = False


class UserCreate(UserBase):
    """Schema for creating a new user"""
    password: str = Field(..., min_length=8, max_length=255)


class UserUpdate(BaseSchema):
    """Schema for updating a user"""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    phone: Optional[str] = Field(None, max_length=20)
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None


class UserResponse(UserBase, BaseResponseSchema):
    """Schema for user responses"""
    pass


class UserList(BaseSchema):
    """Schema for user list responses"""
    users: list[UserResponse]
    total: int