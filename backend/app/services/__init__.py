# Business logic services

from .base import BaseCRUDService
from .campaign import CampaignService, campaign_service
from .client import ClientService, client_service
from .craftsman import CraftsmanService, craftsman_service
from .item import ItemService, item_service
from .project import ProjectService, project_service
from .quote import QuoteService, quote_service
from .task import TaskService, task_service
from .user import UserService, user_service

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
