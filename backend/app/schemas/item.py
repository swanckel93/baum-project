from typing import Optional
from decimal import Decimal
from pydantic import Field
from ..models.enums import Unit
from .base import BaseSchema, BaseResponseSchema


class ItemBase(BaseSchema):
    """Base item schema with common fields"""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    quantity: int = Field(1, gt=0)
    unit: Unit = Unit.UNIT
    estimated_cost: Optional[Decimal] = Field(None, ge=0, decimal_places=2)


class ItemCreate(ItemBase):
    """Schema for creating a new item"""
    campaign_id: int = Field(..., gt=0)


class ItemUpdate(BaseSchema):
    """Schema for updating an item"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    quantity: Optional[int] = Field(None, gt=0)
    unit: Optional[Unit] = None
    estimated_cost: Optional[Decimal] = Field(None, ge=0, decimal_places=2)


class ItemResponse(ItemBase, BaseResponseSchema):
    """Schema for item responses"""
    campaign_id: int


class ItemList(BaseSchema):
    """Schema for item list responses"""
    items: list[ItemResponse]
    total: int