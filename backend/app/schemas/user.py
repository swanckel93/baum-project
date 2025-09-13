from typing import Optional
import re
from pydantic import EmailStr, Field, field_validator, ValidationInfo
from .base import BaseSchema, BaseResponseSchema


class UserBase(BaseSchema):
    """Base user schema with common fields"""
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=255)
    phone: Optional[str] = Field(None, max_length=20)
    is_active: bool = True
    is_admin: bool = False
    
    @field_validator('full_name')
    @classmethod
    def validate_full_name(cls, v: str) -> str:
        """Validate full name contains only letters, spaces, hyphens, and apostrophes"""
        if not v.strip():
            raise ValueError('Full name cannot be empty or only whitespace')
        
        # Allow letters, numbers, spaces, hyphens, apostrophes, and dots
        if not re.match(r"^[a-zA-ZÀ-ÿ0-9\s\-'.]+$", v.strip()):
            raise ValueError('Full name can only contain letters, numbers, spaces, hyphens, apostrophes, and dots')
        
        return v.strip().title()
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        """Validate phone number format"""
        if v is None:
            return v
        
        # Remove all non-digit characters for validation
        digits_only = re.sub(r'\D', '', v)
        
        # Must be between 7 and 15 digits (international standard)
        if len(digits_only) < 7 or len(digits_only) > 15:
            raise ValueError('Phone number must be between 7 and 15 digits')
        
        # Return original format (user can use +, -, spaces, etc.)
        return v.strip()


class UserCreate(UserBase):
    """Schema for creating a new user"""
    password: str = Field(..., min_length=8, max_length=255)
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password strength"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        
        # Check for at least one lowercase letter
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        
        # Check for at least one uppercase letter or digit
        if not re.search(r'[A-Z0-9]', v):
            raise ValueError('Password must contain at least one uppercase letter or digit')
        
        return v


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