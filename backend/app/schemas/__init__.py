# Pydantic schemas for request/response validation

from .base import BaseSchema, BaseResponseSchema, PaginationParams, PaginatedResponse
from .user import UserBase, UserCreate, UserUpdate, UserResponse, UserList
from .client import ClientBase, ClientCreate, ClientUpdate, ClientResponse, ClientList
from .craftsman import CraftsmanBase, CraftsmanCreate, CraftsmanUpdate, CraftsmanResponse, CraftsmanList
from .project import ProjectBase, ProjectCreate, ProjectUpdate, ProjectResponse, ProjectList
from .campaign import CampaignBase, CampaignCreate, CampaignUpdate, CampaignResponse, CampaignList
from .item import ItemBase, ItemCreate, ItemUpdate, ItemResponse, ItemList
from .quote import QuoteBase, QuoteCreate, QuoteUpdate, QuoteResponse, QuoteList
from .task import TaskBase, TaskCreate, TaskUpdate, TaskResponse, TaskList

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