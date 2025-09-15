from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...models.enums import CampaignStatus
from ...schemas.campaign import CampaignCreate, CampaignResponse, CampaignUpdate
from ...services.campaign import campaign_service

router = APIRouter(tags=["campaigns"])


@router.post("/", response_model=CampaignResponse, status_code=status.HTTP_201_CREATED)
def create_campaign(
    *, db: Session = Depends(get_db), campaign_in: CampaignCreate
) -> CampaignResponse:
    """Create new campaign"""
    campaign = campaign_service.create(db=db, obj_in=campaign_in)
    return campaign


@router.get("/{campaign_id}", response_model=CampaignResponse)
def read_campaign(
    *, db: Session = Depends(get_db), campaign_id: int
) -> CampaignResponse:
    """Get campaign by ID"""
    campaign = campaign_service.get(db=db, id=campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign


@router.put("/{campaign_id}", response_model=CampaignResponse)
def update_campaign(
    *, db: Session = Depends(get_db), campaign_id: int, campaign_in: CampaignUpdate
) -> CampaignResponse:
    """Update campaign"""
    campaign = campaign_service.get(db=db, id=campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    campaign = campaign_service.update(db=db, db_obj=campaign, obj_in=campaign_in)
    return campaign


@router.delete("/{campaign_id}")
def delete_campaign(*, db: Session = Depends(get_db), campaign_id: int):
    """Delete campaign"""
    campaign = campaign_service.delete(db=db, id=campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return {"message": "Campaign deleted successfully"}


@router.get("/", response_model=list[CampaignResponse])
def read_campaigns(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    status_filter: CampaignStatus = None,
    active_only: bool = False,
    project_id: int = None,
) -> list[CampaignResponse]:
    """Get campaigns with optional filters"""
    if project_id:
        campaigns = campaign_service.get_by_project(
            db, project_id=project_id, skip=skip, limit=limit
        )
    elif status_filter:
        campaigns = campaign_service.get_by_status(
            db, status=status_filter, skip=skip, limit=limit
        )
    elif active_only:
        campaigns = campaign_service.get_active(db, skip=skip, limit=limit)
    else:
        campaigns = campaign_service.get_multi(db, skip=skip, limit=limit)
    return campaigns


@router.get("/project/{project_id}", response_model=list[CampaignResponse])
def read_campaigns_by_project(
    *, db: Session = Depends(get_db), project_id: int, skip: int = 0, limit: int = 100
) -> list[CampaignResponse]:
    """Get campaigns by project ID"""
    campaigns = campaign_service.get_by_project(
        db, project_id=project_id, skip=skip, limit=limit
    )
    return campaigns
