from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...models.enums import ProjectStatus
from ...schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate
from ...services.project import project_service

router = APIRouter(tags=["projects"])


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    *,
    db: Session = Depends(get_db),
    project_in: ProjectCreate,
    current_user_id: int = 1,  # TODO: Replace with actual auth
) -> ProjectResponse:
    """Create new project"""
    project = project_service.create(db=db, obj_in=project_in, user_id=current_user_id)
    return project


@router.get("/{project_id}", response_model=ProjectResponse)
def read_project(*, db: Session = Depends(get_db), project_id: int) -> ProjectResponse:
    """Get project by ID"""
    project = project_service.get(db=db, id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    *, db: Session = Depends(get_db), project_id: int, project_in: ProjectUpdate
) -> ProjectResponse:
    """Update project"""
    project = project_service.get(db=db, id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    project = project_service.update(db=db, db_obj=project, obj_in=project_in)
    return project


@router.delete("/{project_id}")
def delete_project(*, db: Session = Depends(get_db), project_id: int):
    """Delete project"""
    project = project_service.delete(db=db, id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "Project deleted successfully"}


@router.get("/", response_model=list[ProjectResponse])
def read_projects(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    status_filter: ProjectStatus = None,
    active_only: bool = False,
    user_id: int = None,
    client_id: int = None,
) -> list[ProjectResponse]:
    """Get projects with optional filters"""
    if user_id:
        projects = project_service.get_by_user(
            db, user_id=user_id, skip=skip, limit=limit
        )
    elif client_id:
        projects = project_service.get_by_client(
            db, client_id=client_id, skip=skip, limit=limit
        )
    elif status_filter:
        projects = project_service.get_by_status(
            db, status=status_filter, skip=skip, limit=limit
        )
    elif active_only:
        projects = project_service.get_active(db, skip=skip, limit=limit)
    else:
        projects = project_service.get_multi(db, skip=skip, limit=limit)
    return projects


@router.get("/user/{user_id}", response_model=list[ProjectResponse])
def read_projects_by_user(
    *, db: Session = Depends(get_db), user_id: int, skip: int = 0, limit: int = 100
) -> list[ProjectResponse]:
    """Get projects by user ID"""
    projects = project_service.get_by_user(db, user_id=user_id, skip=skip, limit=limit)
    return projects


@router.get("/client/{client_id}", response_model=list[ProjectResponse])
def read_projects_by_client(
    *, db: Session = Depends(get_db), client_id: int, skip: int = 0, limit: int = 100
) -> list[ProjectResponse]:
    """Get projects by client ID"""
    projects = project_service.get_by_client(
        db, client_id=client_id, skip=skip, limit=limit
    )
    return projects
