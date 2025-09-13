from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...services.client import client_service
from ...schemas.client import ClientCreate, ClientUpdate, ClientResponse

router = APIRouter(tags=["clients"])


@router.post("/", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
def create_client(
    *,
    db: Session = Depends(get_db),
    client_in: ClientCreate
) -> ClientResponse:
    """Create new client"""
    client = client_service.create(db=db, obj_in=client_in)
    return client


@router.get("/{client_id}", response_model=ClientResponse)
def read_client(
    *,
    db: Session = Depends(get_db),
    client_id: int
) -> ClientResponse:
    """Get client by ID"""
    client = client_service.get(db=db, id=client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@router.put("/{client_id}", response_model=ClientResponse)
def update_client(
    *,
    db: Session = Depends(get_db),
    client_id: int,
    client_in: ClientUpdate
) -> ClientResponse:
    """Update client"""
    client = client_service.get(db=db, id=client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    client = client_service.update(db=db, db_obj=client, obj_in=client_in)
    return client


@router.delete("/{client_id}")
def delete_client(
    *,
    db: Session = Depends(get_db),
    client_id: int
):
    """Delete client"""
    client = client_service.delete(db=db, id=client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return {"message": "Client deleted successfully"}


@router.get("/", response_model=List[ClientResponse])
def read_clients(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
) -> List[ClientResponse]:
    """Get clients"""
    clients = client_service.get_multi(db, skip=skip, limit=limit)
    return clients


@router.get("/search/{name}", response_model=List[ClientResponse])
def search_clients_by_name(
    *,
    db: Session = Depends(get_db),
    name: str
) -> List[ClientResponse]:
    """Search clients by name"""
    clients = client_service.search_by_name(db, name=name)
    return clients