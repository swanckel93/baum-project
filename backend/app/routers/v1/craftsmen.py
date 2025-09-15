from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...services.craftsman import craftsman_service
from ...schemas.craftsman import CraftsmanCreate, CraftsmanUpdate, CraftsmanResponse

router = APIRouter(tags=["craftsmen"])


@router.post("/", response_model=CraftsmanResponse, status_code=status.HTTP_201_CREATED)
def create_craftsman(
    *,
    db: Session = Depends(get_db),
    craftsman_in: CraftsmanCreate
) -> CraftsmanResponse:
    """Create new craftsman"""
    craftsman = craftsman_service.create(db=db, obj_in=craftsman_in)
    return craftsman


@router.get("/{craftsman_id}", response_model=CraftsmanResponse)
def read_craftsman(
    *,
    db: Session = Depends(get_db),
    craftsman_id: int
) -> CraftsmanResponse:
    """Get craftsman by ID"""
    craftsman = craftsman_service.get(db=db, id=craftsman_id)
    if not craftsman:
        raise HTTPException(status_code=404, detail="Craftsman not found")
    return craftsman


@router.put("/{craftsman_id}", response_model=CraftsmanResponse)
def update_craftsman(
    *,
    db: Session = Depends(get_db),
    craftsman_id: int,
    craftsman_in: CraftsmanUpdate
) -> CraftsmanResponse:
    """Update craftsman"""
    craftsman = craftsman_service.get(db=db, id=craftsman_id)
    if not craftsman:
        raise HTTPException(status_code=404, detail="Craftsman not found")
    
    craftsman = craftsman_service.update(db=db, db_obj=craftsman, obj_in=craftsman_in)
    return craftsman


@router.delete("/{craftsman_id}")
def delete_craftsman(
    *,
    db: Session = Depends(get_db),
    craftsman_id: int
):
    """Delete craftsman"""
    craftsman = craftsman_service.delete(db=db, id=craftsman_id)
    if not craftsman:
        raise HTTPException(status_code=404, detail="Craftsman not found")
    return {"message": "Craftsman deleted successfully"}


@router.get("/", response_model=List[CraftsmanResponse])
def read_craftsmen(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    active_only: bool = False
) -> List[CraftsmanResponse]:
    """Get craftsmen"""
    if active_only:
        craftsmen = craftsman_service.get_active(db, skip=skip, limit=limit)
    else:
        craftsmen = craftsman_service.get_multi(db, skip=skip, limit=limit)
    return craftsmen


@router.get("/search/specialties/{specialties}", response_model=List[CraftsmanResponse])
def search_craftsmen_by_specialties(
    *,
    db: Session = Depends(get_db),
    specialties: str
) -> List[CraftsmanResponse]:
    """Search craftsmen by specialties"""
    craftsmen = craftsman_service.search_by_specialties(db, specialties=specialties)
    return craftsmen


@router.get("/phone/{phone}", response_model=CraftsmanResponse)
def read_craftsman_by_phone(
    *,
    db: Session = Depends(get_db),
    phone: str
) -> CraftsmanResponse:
    """Get craftsman by phone number"""
    craftsman = craftsman_service.get_by_phone(db, phone=phone)
    if not craftsman:
        raise HTTPException(status_code=404, detail="Craftsman not found")
    return craftsman