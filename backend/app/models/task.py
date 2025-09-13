from typing import Optional
from datetime import date
from sqlalchemy import String, Text, Date, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import BaseModel
from .enums import TaskStatus, TaskPriority

class Task(BaseModel):
    __tablename__ = "tasks"
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[TaskStatus] = mapped_column(Enum(TaskStatus), nullable=False, default=TaskStatus.TODO)
    priority: Mapped[TaskPriority] = mapped_column(Enum(TaskPriority), nullable=False, default=TaskPriority.MEDIUM)
    due_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    
    # Foreign Keys
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    assigned_user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    
    # Relationships
    project = relationship("Project", back_populates="tasks")
    assigned_user = relationship("User", foreign_keys=[assigned_user_id])
    
    def __repr__(self) -> str:
        return f"<Task(id={self.id}, title='{self.title}', status='{self.status}', priority='{self.priority}')>"