from typing import Optional
from datetime import date
from sqlalchemy import String, Text, Numeric, Date, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import BaseModel
from .enums import QuoteStatus, Currency

class Quote(BaseModel):
    __tablename__ = "quotes"
    
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[Currency] = mapped_column(Enum(Currency), nullable=False, default=Currency.EUR)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[QuoteStatus] = mapped_column(Enum(QuoteStatus), nullable=False, default=QuoteStatus.PENDING)
    margin_percentage: Mapped[Optional[float]] = mapped_column(Numeric(5, 2), nullable=True)
    valid_until: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    whatsapp_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Foreign Keys
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"), nullable=False)
    craftsman_id: Mapped[int] = mapped_column(ForeignKey("craftsmen.id"), nullable=False)
    
    # Relationships
    item = relationship("Item", back_populates="quotes")
    craftsman = relationship("Craftsman", back_populates="quotes")
    
    def __repr__(self) -> str:
        return f"<Quote(id={self.id}, price={self.price} {self.currency}, status='{self.status}')>"