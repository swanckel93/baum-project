from typing import Optional
from pydantic import EmailStr, Field
from .base import BaseSchema, BaseResponseSchema


class ClientBase(BaseSchema):
    """Base client schema with common fields"""
    name: str = Field(..., min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None
    notes: Optional[str] = None


class ClientCreate(ClientBase):
    """Schema for creating a new client"""
    pass


class ClientUpdate(BaseSchema):
    """Schema for updating a client"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None
    notes: Optional[str] = None


class ClientResponse(ClientBase, BaseResponseSchema):
    """Schema for client responses"""
    pass


class ClientList(BaseSchema):
    """Schema for client list responses"""
    clients: list[ClientResponse]
    total: int