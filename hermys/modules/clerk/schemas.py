from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from hermys.db.base import ObjectIdField
from hermys.modules.clerk.enums import OpenAiGPTModelEnum


class ClerkBase(BaseModel):
    name: str = Field(default=...)
    description: Optional[str] = Field(default=...)
    prompt: str = Field(default=...)
    gpt_model: OpenAiGPTModelEnum = Field(
        default=OpenAiGPTModelEnum.GOT_35_TURBO,
    )


class ClerkCreatePayload(ClerkBase):
    ...


class ClerkRetrieve(ClerkBase):
    id: ObjectIdField = Field(default=..., alias='_id')
    active: bool = Field(default=...)
    slug: str = Field(default=...)
    photo: Optional[str] = Field(default=None)

    model_config = ConfigDict(populate_by_name=True)


class ClerkUpdatePayload(BaseModel):
    photo: Optional[str] = Field(default=...)
