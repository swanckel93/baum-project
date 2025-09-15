from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """Base schema with common configuration"""

    model_config = ConfigDict(from_attributes=True)


class BaseResponseSchema(BaseSchema):
    """Base response schema with common fields"""

    id: int
    created_at: datetime
    updated_at: datetime | None = None


class PaginationParams(BaseSchema):
    """Pagination parameters for list endpoints"""

    skip: int = 0
    limit: int = 100


class PaginatedResponse(BaseSchema):
    """Generic paginated response"""

    items: list
    total: int
    skip: int
    limit: int
