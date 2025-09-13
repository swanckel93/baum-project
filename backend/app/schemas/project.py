from typing import Optional
from datetime import date
from decimal import Decimal
from pydantic import Field
from ..models.enums import ProjectStatus
from .base import BaseSchema, BaseResponseSchema


class ProjectBase(BaseSchema):
    """Base project schema with common fields"""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    status: ProjectStatus = ProjectStatus.PLANNING
    budget: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class ProjectCreate(ProjectBase):
    """Schema for creating a new project"""
    client_id: int = Field(..., gt=0)


class ProjectUpdate(BaseSchema):
    """Schema for updating a project"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[ProjectStatus] = None
    budget: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    client_id: Optional[int] = Field(None, gt=0)


class ProjectResponse(ProjectBase, BaseResponseSchema):
    """Schema for project responses"""
    user_id: int
    client_id: int


class ProjectList(BaseSchema):
    """Schema for project list responses"""
    projects: list[ProjectResponse]
    total: int