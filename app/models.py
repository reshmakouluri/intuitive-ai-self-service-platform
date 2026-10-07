from datetime import datetime, timezone
from enum import Enum
from uuid import UUID
from pydantic import BaseModel, Field


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class DeploymentState(str, Enum):
    PENDING = "PENDING"
    VALIDATING = "VALIDATING"
    PROVISIONING = "PROVISIONING"
    DEPLOYING = "DEPLOYING"
    HEALTH_CHECKING = "HEALTH_CHECKING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    ROLLING_BACK = "ROLLING_BACK"
    ROLLED_BACK = "ROLLED_BACK"


class DeploymentRequest(BaseModel):
    application: str = Field(min_length=1, max_length=100)
    version: str = Field(min_length=1, max_length=100)
    environment: str = Field(pattern="^(staging)$")
    simulate_failure: bool = False


class Deployment(BaseModel):
    id: UUID
    application: str
    version: str
    environment: str
    state: DeploymentState
    created_at: datetime
    updated_at: datetime
    error: str | None = None


class DeploymentEvent(BaseModel):
    timestamp: datetime
    state: DeploymentState
    message: str
