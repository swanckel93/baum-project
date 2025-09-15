from strenum import StrEnum


class ProjectStatus(StrEnum):
    PLANNING = "planning"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    ON_HOLD = "on hold"


class CampaignStatus(StrEnum):
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    ON_HOLD = "on hold"


class QuoteStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"


class Currency(StrEnum):
    EUR = "EUR"
    USD = "USD"
    GBP = "GBP"


class TaskStatus(StrEnum):
    TODO = "todo"
    IN_PROGRESS = "in progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TaskPriority(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class Unit(StrEnum):
    UNIT = "unit"
    HOUR = "hour"
    SQUARE_METER = "square meter"
    LINEAR_METER = "linear meter"
    KILOGRAM = "kilogram"
    CUBIC_METER = "cubic meter"
