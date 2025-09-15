# Pydantic schemas for request/response validation

from .base import BaseResponseSchema, BaseSchema, PaginatedResponse, PaginationParams
from .campaign import (
    CampaignBase,
    CampaignCreate,
    CampaignList,
    CampaignResponse,
    CampaignUpdate,
)
from .client import ClientBase, ClientCreate, ClientList, ClientResponse, ClientUpdate
from .craftsman import (
    CraftsmanBase,
    CraftsmanCreate,
    CraftsmanList,
    CraftsmanResponse,
    CraftsmanUpdate,
)
from .item import ItemBase, ItemCreate, ItemList, ItemResponse, ItemUpdate
from .project import (
    ProjectBase,
    ProjectCreate,
    ProjectList,
    ProjectResponse,
    ProjectUpdate,
)
from .quote import QuoteBase, QuoteCreate, QuoteList, QuoteResponse, QuoteUpdate
from .task import TaskBase, TaskCreate, TaskList, TaskResponse, TaskUpdate
from .user import UserBase, UserCreate, UserList, UserResponse, UserUpdate

__all__ = [
    # Base schemas
    "BaseSchema",
    "BaseResponseSchema",
    "PaginationParams",
    "PaginatedResponse",
    # User schemas
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserList",
    # Client schemas
    "ClientBase",
    "ClientCreate",
    "ClientUpdate",
    "ClientResponse",
    "ClientList",
    # Craftsman schemas
    "CraftsmanBase",
    "CraftsmanCreate",
    "CraftsmanUpdate",
    "CraftsmanResponse",
    "CraftsmanList",
    # Project schemas
    "ProjectBase",
    "ProjectCreate",
    "ProjectUpdate",
    "ProjectResponse",
    "ProjectList",
    # Campaign schemas
    "CampaignBase",
    "CampaignCreate",
    "CampaignUpdate",
    "CampaignResponse",
    "CampaignList",
    # Item schemas
    "ItemBase",
    "ItemCreate",
    "ItemUpdate",
    "ItemResponse",
    "ItemList",
    # Quote schemas
    "QuoteBase",
    "QuoteCreate",
    "QuoteUpdate",
    "QuoteResponse",
    "QuoteList",
    # Task schemas
    "TaskBase",
    "TaskCreate",
    "TaskUpdate",
    "TaskResponse",
    "TaskList",
]
