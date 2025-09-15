from typing import List
from sqlalchemy.orm import Session
from ..models.campaign import Campaign
from ..models.enums import CampaignStatus
from ..schemas.campaign import CampaignCreate, CampaignUpdate
from .base import BaseCRUDService


class CampaignService(BaseCRUDService[Campaign, CampaignCreate, CampaignUpdate]):
    """Campaign-specific CRUD service"""
    
    def get_by_project(self, db: Session, *, project_id: int, skip: int = 0, limit: int = 100) -> List[Campaign]:
        """Get campaigns by project ID"""
        return db.query(Campaign).filter(
            Campaign.project_id == project_id
        ).offset(skip).limit(limit).all()
    
    def get_by_status(self, db: Session, *, status: CampaignStatus, skip: int = 0, limit: int = 100) -> List[Campaign]:
        """Get campaigns by status"""
        return db.query(Campaign).filter(
            Campaign.status == status
        ).offset(skip).limit(limit).all()
    
    def get_active(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Campaign]:
        """Get active campaigns"""
        return db.query(Campaign).filter(
            Campaign.status == CampaignStatus.ACTIVE
        ).offset(skip).limit(limit).all()


# Create instance
campaign_service = CampaignService(Campaign)