from sqlalchemy.orm import Session

from ..models.client import Client
from ..schemas.client import ClientCreate, ClientUpdate
from .base import BaseCRUDService


class ClientService(BaseCRUDService[Client, ClientCreate, ClientUpdate]):
    """Client-specific CRUD service"""

    def get_by_email(self, db: Session, *, email: str) -> Client | None:
        """Get client by email address"""
        return db.query(Client).filter(Client.email == email).first()

    def search_by_name(self, db: Session, *, name: str) -> list[Client]:
        """Search clients by name (case insensitive)"""
        return db.query(Client).filter(Client.name.ilike(f"%{name}%")).all()


# Create instance
client_service = ClientService(Client)
