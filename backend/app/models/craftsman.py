from sqlalchemy import Boolean, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel


class Craftsman(BaseModel):
    __tablename__ = "craftsmen"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    whatsapp: Mapped[str | None] = mapped_column(String(20), nullable=True)
    specialties: Mapped[str] = mapped_column(String(500), nullable=False)
    hourly_rate: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    quotes = relationship("Quote", back_populates="craftsman")

    def __repr__(self) -> str:
        return f"<Craftsman(id={self.id}, name='{self.name}', specialties='{self.specialties}')>"
