from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...services.quote import quote_service
from ...schemas.quote import QuoteCreate, QuoteUpdate, QuoteResponse
from ...models.enums import QuoteStatus

router = APIRouter(tags=["quotes"])


@router.post("/", response_model=QuoteResponse, status_code=status.HTTP_201_CREATED)
def create_quote(
    *,
    db: Session = Depends(get_db),
    quote_in: QuoteCreate
) -> QuoteResponse:
    """Create new quote"""
    quote = quote_service.create(db=db, obj_in=quote_in)
    return quote


@router.get("/{quote_id}", response_model=QuoteResponse)
def read_quote(
    *,
    db: Session = Depends(get_db),
    quote_id: int
) -> QuoteResponse:
    """Get quote by ID"""
    quote = quote_service.get(db=db, id=quote_id)
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    return quote


@router.put("/{quote_id}", response_model=QuoteResponse)
def update_quote(
    *,
    db: Session = Depends(get_db),
    quote_id: int,
    quote_in: QuoteUpdate
) -> QuoteResponse:
    """Update quote"""
    quote = quote_service.get(db=db, id=quote_id)
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    
    quote = quote_service.update(db=db, db_obj=quote, obj_in=quote_in)
    return quote


@router.delete("/{quote_id}")
def delete_quote(
    *,
    db: Session = Depends(get_db),
    quote_id: int
):
    """Delete quote"""
    quote = quote_service.delete(db=db, id=quote_id)
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    return {"message": "Quote deleted successfully"}


@router.get("/", response_model=List[QuoteResponse])
def read_quotes(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    status_filter: QuoteStatus = None,
    item_id: int = None,
    craftsman_id: int = None,
    pending_only: bool = False,
    approved_only: bool = False
) -> List[QuoteResponse]:
    """Get quotes with optional filters"""
    if item_id:
        quotes = quote_service.get_by_item(db, item_id=item_id, skip=skip, limit=limit)
    elif craftsman_id:
        quotes = quote_service.get_by_craftsman(db, craftsman_id=craftsman_id, skip=skip, limit=limit)
    elif status_filter:
        quotes = quote_service.get_by_status(db, status=status_filter, skip=skip, limit=limit)
    elif pending_only:
        quotes = quote_service.get_pending(db, skip=skip, limit=limit)
    elif approved_only:
        quotes = quote_service.get_approved(db, skip=skip, limit=limit)
    else:
        quotes = quote_service.get_multi(db, skip=skip, limit=limit)
    return quotes


@router.get("/item/{item_id}", response_model=List[QuoteResponse])
def read_quotes_by_item(
    *,
    db: Session = Depends(get_db),
    item_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[QuoteResponse]:
    """Get quotes by item ID"""
    quotes = quote_service.get_by_item(db, item_id=item_id, skip=skip, limit=limit)
    return quotes


@router.get("/craftsman/{craftsman_id}", response_model=List[QuoteResponse])
def read_quotes_by_craftsman(
    *,
    db: Session = Depends(get_db),
    craftsman_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[QuoteResponse]:
    """Get quotes by craftsman ID"""
    quotes = quote_service.get_by_craftsman(db, craftsman_id=craftsman_id, skip=skip, limit=limit)
    return quotes