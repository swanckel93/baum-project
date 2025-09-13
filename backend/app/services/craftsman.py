from typing import Optional, List
from sqlalchemy.orm import Session
from ..models.craftsman import Craftsman
from ..schemas.craftsman import CraftsmanCreate, CraftsmanUpdate
from .base import BaseCRUDService


class CraftsmanService(BaseCRUDService[Craftsman, CraftsmanCreate, CraftsmanUpdate]):
    """Craftsman-specific CRUD service"""
    
    def get_by_phone(self, db: Session, *, phone: str) -> Optional[Craftsman]:
        """Get craftsman by phone number"""
        return db.query(Craftsman).filter(Craftsman.phone == phone).first()
    
    def get_by_whatsapp(self, db: Session, *, whatsapp_number: str) -> Optional[Craftsman]:
        """Get craftsman by WhatsApp number"""
        return db.query(Craftsman).filter(Craftsman.whatsapp_number == whatsapp_number).first()
    
    def get_active(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Craftsman]:
        """Get active craftsmen only"""
        return db.query(Craftsman).filter(
            Craftsman.is_active == True
        ).offset(skip).limit(limit).all()
    
    def search_by_specialty(self, db: Session, *, specialty: str) -> List[Craftsman]:
        """Search craftsmen by specialty (case insensitive)"""
        return db.query(Craftsman).filter(
            Craftsman.specialty.ilike(f"%{specialty}%")
        ).all()


# Create instance
craftsman_service = CraftsmanService(Craftsman)