from typing import Optional
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate
from .base import BaseCRUDService

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService(BaseCRUDService[User, UserCreate, UserUpdate]):
    """User-specific CRUD service with password hashing"""
    
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        """Get user by email address"""
        return db.query(User).filter(User.email == email).first()
    
    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        """Create user with hashed password"""
        obj_data = obj_in.model_dump()
        # Hash the password before storing
        obj_data["hashed_password"] = pwd_context.hash(obj_data.pop("password"))
        
        db_obj = User(**obj_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password"""
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not pwd_context.verify(password, user.hashed_password):
            return None
        return user
    
    def is_active(self, user: User) -> bool:
        """Check if user is active"""
        return user.is_active
    
    def is_admin(self, user: User) -> bool:
        """Check if user is admin"""
        return user.is_admin


# Create instance
user_service = UserService(User)