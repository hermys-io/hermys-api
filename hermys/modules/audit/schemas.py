from datetime import datetime, timezone
from typing import Any, Dict, Optional

from openai import BaseModel
from pydantic import ConfigDict, Field

from hermys.db.base import ObjectIdField
from hermys.modules.audit.enums import (
    AuditActionEnum,
    AuditResourceTypeEnum,
    AuditStatusEnum,
)


class AuditBase(BaseModel):
    user_id: ObjectIdField = Field(default=...)
    user_name: Optional[str] = Field(default=None)
    action: AuditActionEnum = Field(default=...)
    resource_id: ObjectIdField = Field(default=...)
    resource_type: AuditResourceTypeEnum = Field(default=...)
    resource_readebly_name: Optional[str] = Field(default=None)
    status: AuditStatusEnum = Field(default=...)
    metadata: Optional[Dict[str, Any]] = Field(default=None)
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class AuditCreatePayload(AuditBase):
    pass


class AuditInternal(AuditBase):
    id: ObjectIdField = Field(default=..., alias='_id')

    model_config = ConfigDict(populate_by_name=True)
