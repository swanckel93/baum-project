from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...services.item import item_service
from ...schemas.item import ItemCreate, ItemUpdate, ItemResponse

router = APIRouter(tags=["items"])


@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(
    *,
    db: Session = Depends(get_db),
    item_in: ItemCreate
) -> ItemResponse:
    """Create new item"""
    item = item_service.create(db=db, obj_in=item_in)
    return item


@router.get("/{item_id}", response_model=ItemResponse)
def read_item(
    *,
    db: Session = Depends(get_db),
    item_id: int
) -> ItemResponse:
    """Get item by ID"""
    item = item_service.get(db=db, id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.put("/{item_id}", response_model=ItemResponse)
def update_item(
    *,
    db: Session = Depends(get_db),
    item_id: int,
    item_in: ItemUpdate
) -> ItemResponse:
    """Update item"""
    item = item_service.get(db=db, id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    item = item_service.update(db=db, db_obj=item, obj_in=item_in)
    return item


@router.delete("/{item_id}")
def delete_item(
    *,
    db: Session = Depends(get_db),
    item_id: int
):
    """Delete item"""
    item = item_service.delete(db=db, id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}


@router.get("/", response_model=List[ItemResponse])
def read_items(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    campaign_id: int = None
) -> List[ItemResponse]:
    """Get items with optional filters"""
    if campaign_id:
        items = item_service.get_by_campaign(db, campaign_id=campaign_id, skip=skip, limit=limit)
    else:
        items = item_service.get_multi(db, skip=skip, limit=limit)
    return items


@router.get("/campaign/{campaign_id}", response_model=List[ItemResponse])
def read_items_by_campaign(
    *,
    db: Session = Depends(get_db),
    campaign_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[ItemResponse]:
    """Get items by campaign ID"""
    items = item_service.get_by_campaign(db, campaign_id=campaign_id, skip=skip, limit=limit)
    return items


@router.get("/search/{name}", response_model=List[ItemResponse])
def search_items_by_name(
    *,
    db: Session = Depends(get_db),
    name: str
) -> List[ItemResponse]:
    """Search items by name"""
    items = item_service.search_by_name(db, name=name)
    return items