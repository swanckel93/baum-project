from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...schemas.user import UserCreate, UserResponse, UserUpdate
from ...services.user import user_service

router = APIRouter(tags=["users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(*, db: Session = Depends(get_db), user_in: UserCreate) -> UserResponse:
    """Create new user"""
    # Check if user already exists
    if user_service.get_by_email(db, email=user_in.email):
        raise HTTPException(
            status_code=400, detail="User with this email already exists"
        )

    user = user_service.create(db=db, obj_in=user_in)
    return user


@router.get("/{user_id}", response_model=UserResponse)
def read_user(*, db: Session = Depends(get_db), user_id: int) -> UserResponse:
    """Get user by ID"""
    user = user_service.get(db=db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    *, db: Session = Depends(get_db), user_id: int, user_in: UserUpdate
) -> UserResponse:
    """Update user"""
    user = user_service.get(db=db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user = user_service.update(db=db, db_obj=user, obj_in=user_in)
    return user


@router.delete("/{user_id}")
def delete_user(*, db: Session = Depends(get_db), user_id: int):
    """Delete user"""
    user = user_service.delete(db=db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}


@router.get("/", response_model=list[UserResponse])
def read_users(
    db: Session = Depends(get_db), skip: int = 0, limit: int = 100
) -> list[UserResponse]:
    """Get users"""
    users = user_service.get_multi(db, skip=skip, limit=limit)
    return users


@router.get("/email/{email}", response_model=UserResponse)
def read_user_by_email(*, db: Session = Depends(get_db), email: str) -> UserResponse:
    """Get user by email"""
    user = user_service.get_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
