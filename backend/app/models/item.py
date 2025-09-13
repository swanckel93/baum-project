from typing import Optional
from sqlalchemy import String, Text, Integer, Numeric, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import BaseModel
from .enums import Unit

class Item(BaseModel):
    __tablename__ = "items"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    unit: Mapped[Unit] = mapped_column(Enum(Unit), nullable=False, default=Unit.UNIT)
    estimated_cost: Mapped[Optional[float]] = mapped_column(Numeric(10, 2), nullable=True)
    
    # Foreign Keys
    campaign_id: Mapped[int] = mapped_column(ForeignKey("campaigns.id"), nullable=False)
    
    # Relationships
    campaign = relationship("Campaign", back_populates="items")
    quotes = relationship("Quote", back_populates="item", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Item(id={self.id}, name='{self.name}', quantity={self.quantity}, unit='{self.unit}')>"