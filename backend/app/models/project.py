from datetime import date

from sqlalchemy import Date, Enum, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel
from .enums import ProjectStatus


class Project(BaseModel):
    __tablename__ = "projects"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[ProjectStatus] = mapped_column(
        Enum(ProjectStatus), nullable=False, default=ProjectStatus.PLANNING
    )
    budget: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    # Foreign Keys
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="projects")
    client = relationship("Client", back_populates="projects")
    campaigns = relationship(
        "Campaign", back_populates="project", cascade="all, delete-orphan"
    )
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Project(id={self.id}, name='{self.name}', status='{self.status}')>"
