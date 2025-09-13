from typing import Optional
from sqlalchemy import String, Text, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import BaseModel
from .enums import CampaignStatus

class Campaign(BaseModel):
    __tablename__ = "campaigns"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[CampaignStatus] = mapped_column(Enum(CampaignStatus), nullable=False, default=CampaignStatus.ACTIVE)
    
    # Foreign Keys
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    
    # Relationships
    project = relationship("Project", back_populates="campaigns")
    items = relationship("Item", back_populates="campaign", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Campaign(id={self.id}, name='{self.name}', status='{self.status}')>"