from typing import Optional
from pydantic import Field
from ..models.enums import CampaignStatus
from .base import BaseSchema, BaseResponseSchema


class CampaignBase(BaseSchema):
    """Base campaign schema with common fields"""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    status: CampaignStatus = CampaignStatus.ACTIVE


class CampaignCreate(CampaignBase):
    """Schema for creating a new campaign"""
    project_id: int = Field(..., gt=0)


class CampaignUpdate(BaseSchema):
    """Schema for updating a campaign"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[CampaignStatus] = None


class CampaignResponse(CampaignBase, BaseResponseSchema):
    """Schema for campaign responses"""
    project_id: int


class CampaignList(BaseSchema):
    """Schema for campaign list responses"""
    campaigns: list[CampaignResponse]
    total: int