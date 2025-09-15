from typing import Optional
from datetime import date, datetime
from decimal import Decimal
import re
from pydantic import Field, field_validator, model_validator
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
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate project name"""
        if not v.strip():
            raise ValueError('Project name cannot be empty or only whitespace')
        return v.strip()
    
    @field_validator('description')
    @classmethod
    def validate_description(cls, v: Optional[str]) -> Optional[str]:
        """Validate project description"""
        if v is not None and not v.strip():
            return None  # Convert empty strings to None
        return v.strip() if v else v
    
    @field_validator('budget')
    @classmethod
    def validate_budget(cls, v: Optional[Decimal]) -> Optional[Decimal]:
        """Validate budget is positive"""
        if v is not None and v <= 0:
            raise ValueError('Budget must be greater than 0')
        return v
    
    @field_validator('start_date')
    @classmethod
    def validate_start_date(cls, v: Optional[date]) -> Optional[date]:
        """Validate start date is not too far in the past"""
        if v is not None:
            # Don't allow start dates more than 5 years in the past
            min_date = datetime.now().date().replace(year=datetime.now().year - 5)
            if v < min_date:
                raise ValueError('Start date cannot be more than 5 years in the past')
        return v
    
    @model_validator(mode='after')
    def validate_date_range(self):
        """Validate that end_date is after start_date"""
        if self.start_date and self.end_date:
            if self.end_date <= self.start_date:
                raise ValueError('End date must be after start date')
        return self


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