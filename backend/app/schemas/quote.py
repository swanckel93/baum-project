from typing import Optional
from datetime import date, datetime
from decimal import Decimal
from pydantic import Field, field_validator
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
    
    @field_validator('price')
    @classmethod
    def validate_price(cls, v: Decimal) -> Decimal:
        """Validate price is reasonable"""
        if v > 1000000:  # 1 million limit
            raise ValueError('Price cannot exceed 1,000,000')
        return v
    
    @field_validator('valid_until')
    @classmethod
    def validate_valid_until(cls, v: Optional[date]) -> Optional[date]:
        """Validate quote expiration date"""
        if v is not None:
            today = datetime.now().date()
            if v <= today:
                raise ValueError('Quote expiration date must be in the future')
            # Don't allow quotes valid for more than 1 year
            max_date = datetime.now().date().replace(year=datetime.now().year + 1)
            if v > max_date:
                raise ValueError('Quote cannot be valid for more than 1 year')
        return v
    
    @field_validator('whatsapp_message')
    @classmethod
    def validate_whatsapp_message(cls, v: Optional[str]) -> Optional[str]:
        """Validate WhatsApp message length"""
        if v is not None:
            if len(v.strip()) > 4096:  # WhatsApp message limit
                raise ValueError('WhatsApp message cannot exceed 4096 characters')
            return v.strip() if v.strip() else None
        return v


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