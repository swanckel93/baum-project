from typing import Optional
from sqlalchemy import String, Text, Numeric, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import BaseModel

class Craftsman(BaseModel):
    __tablename__ = "craftsmen"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    whatsapp: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    specialties: Mapped[str] = mapped_column(String(500), nullable=False)
    hourly_rate: Mapped[Optional[float]] = mapped_column(Numeric(10, 2), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # Relationships
    quotes = relationship("Quote", back_populates="craftsman")
    
    def __repr__(self) -> str:
        return f"<Craftsman(id={self.id}, name='{self.name}', specialties='{self.specialties}')>"