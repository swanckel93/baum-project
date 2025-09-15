from datetime import date

from pydantic import Field

from ..models.enums import TaskPriority, TaskStatus
from .base import BaseResponseSchema, BaseSchema


class TaskBase(BaseSchema):
    """Base task schema with common fields"""

    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: date | None = None


class TaskCreate(TaskBase):
    """Schema for creating a new task"""

    project_id: int = Field(..., gt=0)
    assigned_user_id: int | None = Field(None, gt=0)


class TaskUpdate(BaseSchema):
    """Schema for updating a task"""

    title: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    due_date: date | None = None
    assigned_user_id: int | None = Field(None, gt=0)


class TaskResponse(TaskBase, BaseResponseSchema):
    """Schema for task responses"""

    project_id: int
    assigned_user_id: int | None = None


class TaskList(BaseSchema):
    """Schema for task list responses"""

    tasks: list[TaskResponse]
    total: int
