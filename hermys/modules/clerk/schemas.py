from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from hermys.db.base import ObjectIdField


class ClerkBase(BaseModel):
    name: str = Field(default=...)
    description: Optional[str] = Field(default=...)
    prompt: str = Field(default=...)


class ClerkCreatePayload(ClerkBase):
    ...


class ClerkRetrieve(ClerkBase):
    id: ObjectIdField = Field(default=..., alias='_id')
    active: bool = Field(default=...)
    slug: str = Field(default=...)

    model_config = ConfigDict(populate_by_name=True)
