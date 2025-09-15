from sqlalchemy.orm import Session

from ..models.enums import QuoteStatus
from ..models.quote import Quote
from ..schemas.quote import QuoteCreate, QuoteUpdate
from .base import BaseCRUDService


class QuoteService(BaseCRUDService[Quote, QuoteCreate, QuoteUpdate]):
    """Quote-specific CRUD service"""

    def get_by_item(
        self, db: Session, *, item_id: int, skip: int = 0, limit: int = 100
    ) -> list[Quote]:
        """Get quotes by item ID"""
        return (
            db.query(Quote)
            .filter(Quote.item_id == item_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_craftsman(
        self, db: Session, *, craftsman_id: int, skip: int = 0, limit: int = 100
    ) -> list[Quote]:
        """Get quotes by craftsman ID"""
        return (
            db.query(Quote)
            .filter(Quote.craftsman_id == craftsman_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_status(
        self, db: Session, *, status: QuoteStatus, skip: int = 0, limit: int = 100
    ) -> list[Quote]:
        """Get quotes by status"""
        return (
            db.query(Quote)
            .filter(Quote.status == status)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_pending(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> list[Quote]:
        """Get pending quotes"""
        return (
            db.query(Quote)
            .filter(Quote.status == QuoteStatus.PENDING)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_approved(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> list[Quote]:
        """Get approved quotes"""
        return (
            db.query(Quote)
            .filter(Quote.status == QuoteStatus.APPROVED)
            .offset(skip)
            .limit(limit)
            .all()
        )


# Create instance
quote_service = QuoteService(Quote)
