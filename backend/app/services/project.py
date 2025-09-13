from typing import List
from sqlalchemy.orm import Session
from ..models.project import Project
from ..models.enums import ProjectStatus
from ..schemas.project import ProjectCreate, ProjectUpdate
from .base import BaseCRUDService


class ProjectService(BaseCRUDService[Project, ProjectCreate, ProjectUpdate]):
    """Project-specific CRUD service"""
    
    def create(self, db: Session, *, obj_in: ProjectCreate, user_id: int) -> Project:
        """Create project with user_id"""
        obj_data = obj_in.model_dump()
        obj_data["user_id"] = user_id
        
        db_obj = Project(**obj_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_by_user(self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100) -> List[Project]:
        """Get projects by user ID"""
        return db.query(Project).filter(
            Project.user_id == user_id
        ).offset(skip).limit(limit).all()
    
    def get_by_client(self, db: Session, *, client_id: int, skip: int = 0, limit: int = 100) -> List[Project]:
        """Get projects by client ID"""
        return db.query(Project).filter(
            Project.client_id == client_id
        ).offset(skip).limit(limit).all()
    
    def get_by_status(self, db: Session, *, status: ProjectStatus, skip: int = 0, limit: int = 100) -> List[Project]:
        """Get projects by status"""
        return db.query(Project).filter(
            Project.status == status
        ).offset(skip).limit(limit).all()
    
    def get_active(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Project]:
        """Get active projects (not completed or cancelled)"""
        return db.query(Project).filter(
            Project.status.in_([ProjectStatus.PLANNING, ProjectStatus.ACTIVE, ProjectStatus.ON_HOLD])
        ).offset(skip).limit(limit).all()


# Create instance
project_service = ProjectService(Project)