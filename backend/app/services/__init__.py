# Business logic services

from .base import BaseCRUDService
from .user import user_service, UserService
from .client import client_service, ClientService
from .craftsman import craftsman_service, CraftsmanService
from .project import project_service, ProjectService
from .campaign import campaign_service, CampaignService
from .item import item_service, ItemService
from .quote import quote_service, QuoteService
from .task import task_service, TaskService

__all__ = [
    # Base service
    "BaseCRUDService",
    # Service classes
    "UserService",
    "ClientService", 
    "CraftsmanService",
    "ProjectService",
    "CampaignService",
    "ItemService",
    "QuoteService",
    "TaskService",
    # Service instances
    "user_service",
    "client_service",
    "craftsman_service", 
    "project_service",
    "campaign_service",
    "item_service",
    "quote_service",
    "task_service",
]