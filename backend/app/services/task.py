from sqlalchemy.orm import Session

from ..models.enums import TaskPriority, TaskStatus
from ..models.task import Task
from ..schemas.task import TaskCreate, TaskUpdate
from .base import BaseCRUDService


class TaskService(BaseCRUDService[Task, TaskCreate, TaskUpdate]):
    """Task-specific CRUD service"""

    def get_by_project(
        self, db: Session, *, project_id: int, skip: int = 0, limit: int = 100
    ) -> list[Task]:
        """Get tasks by project ID"""
        return (
            db.query(Task)
            .filter(Task.project_id == project_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_user(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> list[Task]:
        """Get tasks assigned to user"""
        return (
            db.query(Task)
            .filter(Task.assigned_user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_status(
        self, db: Session, *, status: TaskStatus, skip: int = 0, limit: int = 100
    ) -> list[Task]:
        """Get tasks by status"""
        return (
            db.query(Task).filter(Task.status == status).offset(skip).limit(limit).all()
        )

    def get_by_priority(
        self, db: Session, *, priority: TaskPriority, skip: int = 0, limit: int = 100
    ) -> list[Task]:
        """Get tasks by priority"""
        return (
            db.query(Task)
            .filter(Task.priority == priority)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_todo(self, db: Session, *, skip: int = 0, limit: int = 100) -> list[Task]:
        """Get TODO tasks"""
        return (
            db.query(Task)
            .filter(Task.status == TaskStatus.TODO)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_in_progress(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> list[Task]:
        """Get in-progress tasks"""
        return (
            db.query(Task)
            .filter(Task.status == TaskStatus.IN_PROGRESS)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_unassigned(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> list[Task]:
        """Get unassigned tasks"""
        return (
            db.query(Task)
            .filter(Task.assigned_user_id.is_(None))
            .offset(skip)
            .limit(limit)
            .all()
        )


# Create instance
task_service = TaskService(Task)
