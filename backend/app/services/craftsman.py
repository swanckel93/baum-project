from sqlalchemy.orm import Session

from ..models.craftsman import Craftsman
from ..schemas.craftsman import CraftsmanCreate, CraftsmanUpdate
from .base import BaseCRUDService


class CraftsmanService(BaseCRUDService[Craftsman, CraftsmanCreate, CraftsmanUpdate]):
    """Craftsman-specific CRUD service"""

    def get_by_phone(self, db: Session, *, phone: str) -> Craftsman | None:
        """Get craftsman by phone number"""
        return db.query(Craftsman).filter(Craftsman.phone == phone).first()

    def get_by_whatsapp(self, db: Session, *, whatsapp: str) -> Craftsman | None:
        """Get craftsman by WhatsApp number"""
        return db.query(Craftsman).filter(Craftsman.whatsapp == whatsapp).first()

    def get_active(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> list[Craftsman]:
        """Get active craftsmen only"""
        return (
            db.query(Craftsman)
            .filter(Craftsman.is_active)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def search_by_specialties(
        self, db: Session, *, specialties: str
    ) -> list[Craftsman]:
        """Search craftsmen by specialties (case insensitive)"""
        return (
            db.query(Craftsman)
            .filter(Craftsman.specialties.ilike(f"%{specialties}%"))
            .all()
        )


# Create instance
craftsman_service = CraftsmanService(Craftsman)
