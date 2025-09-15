from pydantic import EmailStr, Field

from .base import BaseResponseSchema, BaseSchema


class ClientBase(BaseSchema):
    """Base client schema with common fields"""

    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr | None = None
    phone: str | None = Field(None, max_length=20)
    address: str | None = None
    notes: str | None = None


class ClientCreate(ClientBase):
    """Schema for creating a new client"""

    pass


class ClientUpdate(BaseSchema):
    """Schema for updating a client"""

    name: str | None = Field(None, min_length=1, max_length=255)
    email: EmailStr | None = None
    phone: str | None = Field(None, max_length=20)
    address: str | None = None
    notes: str | None = None


class ClientResponse(ClientBase, BaseResponseSchema):
    """Schema for client responses"""

    pass


class ClientList(BaseSchema):
    """Schema for client list responses"""

    clients: list[ClientResponse]
    total: int
