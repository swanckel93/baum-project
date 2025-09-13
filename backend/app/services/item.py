from typing import List
from sqlalchemy.orm import Session
from ..models.item import Item
from ..schemas.item import ItemCreate, ItemUpdate
from .base import BaseCRUDService


class ItemService(BaseCRUDService[Item, ItemCreate, ItemUpdate]):
    """Item-specific CRUD service"""
    
    def get_by_campaign(self, db: Session, *, campaign_id: int, skip: int = 0, limit: int = 100) -> List[Item]:
        """Get items by campaign ID"""
        return db.query(Item).filter(
            Item.campaign_id == campaign_id
        ).offset(skip).limit(limit).all()
    
    def search_by_name(self, db: Session, *, name: str) -> List[Item]:
        """Search items by name (case insensitive)"""
        return db.query(Item).filter(
            Item.name.ilike(f"%{name}%")
        ).all()


# Create instance
item_service = ItemService(Item)