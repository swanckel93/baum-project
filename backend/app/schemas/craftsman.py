from typing import Optional
from pydantic import EmailStr, Field
from .base import BaseSchema, BaseResponseSchema


class CraftsmanBase(BaseSchema):
    """Base craftsman schema with common fields"""
    name: str = Field(..., min_length=1, max_length=255)
    specialty: str = Field(..., min_length=1, max_length=255)
    phone: str = Field(..., max_length=20)
    email: Optional[EmailStr] = None
    whatsapp_number: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None
    notes: Optional[str] = None
    is_active: bool = True


class CraftsmanCreate(CraftsmanBase):
    """Schema for creating a new craftsman"""
    pass


class CraftsmanUpdate(BaseSchema):
    """Schema for updating a craftsman"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    specialty: Optional[str] = Field(None, min_length=1, max_length=255)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    whatsapp_number: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None


class CraftsmanResponse(CraftsmanBase, BaseResponseSchema):
    """Schema for craftsman responses"""
    pass


class CraftsmanList(BaseSchema):
    """Schema for craftsman list responses"""
    craftsmen: list[CraftsmanResponse]
    total: int