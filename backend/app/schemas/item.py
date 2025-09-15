from decimal import Decimal

from pydantic import Field

from ..models.enums import Unit
from .base import BaseResponseSchema, BaseSchema


class ItemBase(BaseSchema):
    """Base item schema with common fields"""

    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    quantity: int = Field(1, gt=0)
    unit: Unit = Unit.UNIT
    estimated_cost: Decimal | None = Field(None, ge=0, decimal_places=2)


class ItemCreate(ItemBase):
    """Schema for creating a new item"""

    campaign_id: int = Field(..., gt=0)


class ItemUpdate(BaseSchema):
    """Schema for updating an item"""

    name: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    quantity: int | None = Field(None, gt=0)
    unit: Unit | None = None
    estimated_cost: Decimal | None = Field(None, ge=0, decimal_places=2)


class ItemResponse(ItemBase, BaseResponseSchema):
    """Schema for item responses"""

    campaign_id: int


class ItemList(BaseSchema):
    """Schema for item list responses"""

    items: list[ItemResponse]
    total: int
