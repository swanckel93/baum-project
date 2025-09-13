from typing import Optional
from datetime import date
from pydantic import Field
from ..models.enums import TaskStatus, TaskPriority
from .base import BaseSchema, BaseResponseSchema


class TaskBase(BaseSchema):
    """Base task schema with common fields"""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[date] = None


class TaskCreate(TaskBase):
    """Schema for creating a new task"""
    project_id: int = Field(..., gt=0)
    assigned_user_id: Optional[int] = Field(None, gt=0)


class TaskUpdate(BaseSchema):
    """Schema for updating a task"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[date] = None
    assigned_user_id: Optional[int] = Field(None, gt=0)


class TaskResponse(TaskBase, BaseResponseSchema):
    """Schema for task responses"""
    project_id: int
    assigned_user_id: Optional[int] = None


class TaskList(BaseSchema):
    """Schema for task list responses"""
    tasks: list[TaskResponse]
    total: int