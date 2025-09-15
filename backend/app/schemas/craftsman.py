from typing import Optional
from decimal import Decimal
import re
from pydantic import EmailStr, Field, field_validator
from .base import BaseSchema, BaseResponseSchema


class CraftsmanBase(BaseSchema):
    """Base craftsman schema with common fields"""
    name: str = Field(..., min_length=1, max_length=255)
    specialties: str = Field(..., min_length=1, max_length=500)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    whatsapp: Optional[str] = Field(None, max_length=20)
    hourly_rate: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    notes: Optional[str] = None
    is_active: bool = True
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate craftsman name"""
        if not v.strip():
            raise ValueError('Name cannot be empty or only whitespace')
        # Allow letters, numbers, spaces, hyphens, apostrophes, and dots
        if not re.match(r"^[a-zA-ZÀ-ÿ0-9\s\-'.]+$", v.strip()):
            raise ValueError('Name can only contain letters, numbers, spaces, hyphens, apostrophes, and dots')
        return v.strip().title()
    
    @field_validator('specialties')
    @classmethod
    def validate_specialties(cls, v: str) -> str:
        """Validate specialties field"""
        if not v.strip():
            raise ValueError('Specialties cannot be empty or only whitespace')
        return v.strip()
    
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
    
    @field_validator('whatsapp')
    @classmethod
    def validate_whatsapp(cls, v: Optional[str]) -> Optional[str]:
        """Validate WhatsApp number format"""
        if v is None:
            return v
        
        # Remove all non-digit characters for validation
        digits_only = re.sub(r'\D', '', v)
        
        # Must be between 7 and 15 digits (international standard)
        if len(digits_only) < 7 or len(digits_only) > 15:
            raise ValueError('WhatsApp number must be between 7 and 15 digits')
        
        # Return original format (user can use +, -, spaces, etc.)
        return v.strip()
    
    @field_validator('hourly_rate')
    @classmethod
    def validate_hourly_rate(cls, v: Optional[Decimal]) -> Optional[Decimal]:
        """Validate hourly rate is reasonable"""
        if v is not None:
            if v > 1000:  # $1000/hour max
                raise ValueError('Hourly rate cannot exceed 1000')
        return v


class CraftsmanCreate(CraftsmanBase):
    """Schema for creating a new craftsman"""
    pass


class CraftsmanUpdate(BaseSchema):
    """Schema for updating a craftsman"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    specialties: Optional[str] = Field(None, min_length=1, max_length=500)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    whatsapp: Optional[str] = Field(None, max_length=20)
    hourly_rate: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    notes: Optional[str] = None
    is_active: Optional[bool] = None


class CraftsmanResponse(CraftsmanBase, BaseResponseSchema):
    """Schema for craftsman responses"""
    pass


class CraftsmanList(BaseSchema):
    """Schema for craftsman list responses"""
    craftsmen: list[CraftsmanResponse]
    total: int