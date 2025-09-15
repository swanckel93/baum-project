from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...services.task import task_service
from ...schemas.task import TaskCreate, TaskUpdate, TaskResponse
from ...models.enums import TaskStatus, TaskPriority

router = APIRouter(tags=["tasks"])


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    *,
    db: Session = Depends(get_db),
    task_in: TaskCreate
) -> TaskResponse:
    """Create new task"""
    task = task_service.create(db=db, obj_in=task_in)
    return task


@router.get("/{task_id}", response_model=TaskResponse)
def read_task(
    *,
    db: Session = Depends(get_db),
    task_id: int
) -> TaskResponse:
    """Get task by ID"""
    task = task_service.get(db=db, id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    *,
    db: Session = Depends(get_db),
    task_id: int,
    task_in: TaskUpdate
) -> TaskResponse:
    """Update task"""
    task = task_service.get(db=db, id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = task_service.update(db=db, db_obj=task, obj_in=task_in)
    return task


@router.delete("/{task_id}")
def delete_task(
    *,
    db: Session = Depends(get_db),
    task_id: int
):
    """Delete task"""
    task = task_service.delete(db=db, id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}


@router.get("/", response_model=List[TaskResponse])
def read_tasks(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    status_filter: TaskStatus = None,
    priority_filter: TaskPriority = None,
    project_id: int = None,
    user_id: int = None,
    todo_only: bool = False,
    in_progress_only: bool = False,
    unassigned_only: bool = False
) -> List[TaskResponse]:
    """Get tasks with optional filters"""
    if project_id:
        tasks = task_service.get_by_project(db, project_id=project_id, skip=skip, limit=limit)
    elif user_id:
        tasks = task_service.get_by_user(db, user_id=user_id, skip=skip, limit=limit)
    elif status_filter:
        tasks = task_service.get_by_status(db, status=status_filter, skip=skip, limit=limit)
    elif priority_filter:
        tasks = task_service.get_by_priority(db, priority=priority_filter, skip=skip, limit=limit)
    elif todo_only:
        tasks = task_service.get_todo(db, skip=skip, limit=limit)
    elif in_progress_only:
        tasks = task_service.get_in_progress(db, skip=skip, limit=limit)
    elif unassigned_only:
        tasks = task_service.get_unassigned(db, skip=skip, limit=limit)
    else:
        tasks = task_service.get_multi(db, skip=skip, limit=limit)
    return tasks


@router.get("/project/{project_id}", response_model=List[TaskResponse])
def read_tasks_by_project(
    *,
    db: Session = Depends(get_db),
    project_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[TaskResponse]:
    """Get tasks by project ID"""
    tasks = task_service.get_by_project(db, project_id=project_id, skip=skip, limit=limit)
    return tasks


@router.get("/user/{user_id}", response_model=List[TaskResponse])
def read_tasks_by_user(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[TaskResponse]:
    """Get tasks assigned to user"""
    tasks = task_service.get_by_user(db, user_id=user_id, skip=skip, limit=limit)
    return tasks