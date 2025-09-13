from typing import Optional
from datetime import date
from decimal import Decimal
from pydantic import Field
from ..models.enums import QuoteStatus, Currency
from .base import BaseSchema, BaseResponseSchema


class QuoteBase(BaseSchema):
    """Base quote schema with common fields"""
    price: Decimal = Field(..., gt=0, decimal_places=2)
    currency: Currency = Currency.EUR
    description: Optional[str] = None
    status: QuoteStatus = QuoteStatus.PENDING
    margin_percentage: Optional[Decimal] = Field(None, ge=0, le=100, decimal_places=2)
    valid_until: Optional[date] = None
    whatsapp_message: Optional[str] = None


class QuoteCreate(QuoteBase):
    """Schema for creating a new quote"""
    item_id: int = Field(..., gt=0)
    craftsman_id: int = Field(..., gt=0)


class QuoteUpdate(BaseSchema):
    """Schema for updating a quote"""
    price: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    currency: Optional[Currency] = None
    description: Optional[str] = None
    status: Optional[QuoteStatus] = None
    margin_percentage: Optional[Decimal] = Field(None, ge=0, le=100, decimal_places=2)
    valid_until: Optional[date] = None
    whatsapp_message: Optional[str] = None


class QuoteResponse(QuoteBase, BaseResponseSchema):
    """Schema for quote responses"""
    item_id: int
    craftsman_id: int


class QuoteList(BaseSchema):
    """Schema for quote list responses"""
    quotes: list[QuoteResponse]
    total: int