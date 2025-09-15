from pydantic import Field

from ..models.enums import CampaignStatus
from .base import BaseResponseSchema, BaseSchema


class CampaignBase(BaseSchema):
    """Base campaign schema with common fields"""

    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    status: CampaignStatus = CampaignStatus.ACTIVE


class CampaignCreate(CampaignBase):
    """Schema for creating a new campaign"""

    project_id: int = Field(..., gt=0)


class CampaignUpdate(BaseSchema):
    """Schema for updating a campaign"""

    name: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    status: CampaignStatus | None = None


class CampaignResponse(CampaignBase, BaseResponseSchema):
    """Schema for campaign responses"""

    project_id: int


class CampaignList(BaseSchema):
    """Schema for campaign list responses"""

    campaigns: list[CampaignResponse]
    total: int
